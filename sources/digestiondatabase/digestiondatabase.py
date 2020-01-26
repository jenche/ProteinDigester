import sqlite3
import uuid
from collections import namedtuple
from pathlib import Path
from time import time
from typing import List, Tuple, Union, Iterator, Callable, Optional

from digestiondatabase import digester, fastareader

DigestionSettings = namedtuple('DigestionSettings', ('enzyme', 'missed_cleavages'))
Protein = namedtuple('Protein', ('id', 'name', 'sequence'))
Peptide = namedtuple('Peptide', ('id', 'sequence', 'missed_cleavages', 'is_unique'))
DigestionTables = namedtuple('DigestionTables', ('peptides_table', 'peptides_association'))


class DigestionAlreadyExistsError(Exception):
    pass


class DigestionDoesntExistError(Exception):
    pass


class ResultsLimitExceededError(Exception):
    pass


class DigestionDatabase:
    def __init__(self, database_path: Union[Path, str], create=False, overwrite=False) -> None:
        self._last_progress_handler_call: Optional[float] = None
        self._current_task_iteration = 0
        self._maximum_task_iteration = 0
        self._current_task = ''
        self._progress_handler_function: Optional[Callable] = None

        path = Path(database_path)

        if path.exists() and path.is_file():
            if create:
                if overwrite:
                    Path(database_path).unlink()
                else:
                    raise FileExistsError

        elif not create:
            raise FileNotFoundError

        self._path = database_path

        try:
            self._connection = sqlite3.connect(str(database_path))
        except sqlite3.OperationalError:
            raise IOError

        self._connection.row_factory = sqlite3.Row
        self._connection.set_progress_handler(self._progress_handler, 1000)

        if create:
            with self._connection:
                self._connection.execute('PRAGMA journal_mode=WAL')

                self._connection.execute('''CREATE TABLE sequences(
                                            id INTEGER,
                                            sequence TEXT NOT NULL UNIQUE,
                                            PRIMARY KEY(id))''')

                self._connection.execute('''CREATE TABLE proteins(
                                            id INTEGER,
                                            name TEXT NOT NULL UNIQUE,
                                            sequence_id INTEGER NOT NULL,
                                            FOREIGN KEY(sequence_id) REFERENCES sequences(id)
                                            PRIMARY KEY(id))''')

                self._connection.execute('''CREATE TABLE digestions(
                                            enzyme TEXT NOT NULL,
                                            missed_cleavages INTEGER NOT NULL,
                                            peptides_table TEXT NOT NULL)''')

    def _progress_handler(self) -> bool:
        if self._progress_handler_function:
            time_condition = not self._last_progress_handler_call or (time() - self._last_progress_handler_call > 0.2)
            iteration_condition = self._current_task_iteration == -1

            if time_condition or iteration_condition:
                self._last_progress_handler_call = time()
                return self._progress_handler_function(self._current_task,
                                                       self._current_task_iteration,
                                                       self._maximum_task_iteration)
        else:
            self._last_progress_handler_call = None
            return False

    def _end_of_task(self) -> None:
        self._current_task_iteration = -1
        self._maximum_task_iteration = -1
        self._progress_handler()
        self._progress_handler_function = None

    def close(self) -> None:
        self._connection.close()
        self._connection = None
        self._path = None

    @property
    def path(self) -> Path:
        return self._path

    def _digestion_tables(self, enzyme: str, missed_cleavages: int) -> DigestionTables:
        if not self._connection:
            raise RuntimeError('No database is opened')

        if DigestionSettings(enzyme, missed_cleavages) not in self.available_digestions:
            raise DigestionDoesntExistError('Digestion doesn\'t exist')

        cursor = self._connection.execute('''SELECT peptides_table FROM digestions 
                                             WHERE enzyme = ? AND missed_cleavages = ?''',
                                          (enzyme, missed_cleavages))
        digestion_tables = cursor.fetchone()['peptides_table']
        return DigestionTables(f'"{digestion_tables}"',
                               f'"{digestion_tables + "_association"}"')

    @property
    def available_digestion_enzymes(self) -> List[str]:
        return digester.available_enzymes()

    @property
    def available_digestions(self) -> Tuple[DigestionSettings]:
        if not self._connection:
            raise RuntimeError('No database is opened')

        cursor = self._connection.execute('SELECT enzyme, missed_cleavages FROM digestions')
        available_digestions = [DigestionSettings(row['enzyme'], row['missed_cleavages']) for row in cursor]
        available_digestions.sort(key=lambda digestion: digestion.missed_cleavages)
        available_digestions.sort(key=lambda digestion: digestion.enzyme)
        return tuple(available_digestions)

    @property
    def proteins_count(self) -> int:
        if not self._connection:
            raise RuntimeError('No database is opened')

        cursor = self._connection.execute('SELECT COUNT(*) FROM proteins')
        return cursor.fetchone()[0]

    @property
    def sequences_count(self) -> int:
        if not self._connection:
            raise RuntimeError('No database is opened')

        cursor = self._connection.execute('SELECT COUNT(*) FROM sequences')
        return cursor.fetchone()[0]

    def import_database(self, filename: Union[Path, str], callback=None) -> None:
        def handle_callback(progress, maximum):
            self._current_task_iteration = progress
            self._maximum_task_iteration = maximum

        if not self._connection:
            raise RuntimeError('No database is opened')

        self._current_task = 'Importing FASTA file...'
        self._progress_handler_function = callback

        with self._connection:
            try:
                for i, (name, sequence) in enumerate(fastareader.read(str(filename), handle_callback), start=1):
                    self._connection.execute('INSERT INTO sequences(sequence) VALUES(?) ON CONFLICT DO NOTHING',
                                             (sequence,))
                    cursor = self._connection.execute('SELECT id FROM sequences WHERE sequence = ?', (sequence,))
                    self._connection.execute(
                        'INSERT INTO proteins(name, sequence_id) VALUES(?, ?) ON CONFLICT DO NOTHING',
                        (name, cursor.fetchone()['id']))

                for digestion in self.available_digestions:
                    self._digest(digestion.enzyme, digestion.missed_cleavages, callback=callback)

            except sqlite3.OperationalError:
                # Callbacks has returned a non-null value
                self._connection.rollback()
            finally:
                self._end_of_task()

    def add_digestion(self, enzyme, missed_cleavages, callback=None, proteins_per_batch=10000) -> None:
        # Checks if the digestion already exists
        if DigestionSettings(enzyme, missed_cleavages) in self.available_digestions:
            raise DigestionAlreadyExistsError('Digestion already exists')

        # Generates a uuid as the table name
        digestion_table_name = uuid.uuid4().hex

        # Add this digestion table into the list of digestion
        self._connection.execute('INSERT INTO digestions(enzyme, missed_cleavages, peptides_table) VALUES(?, ?, ?)',
                                 (enzyme, missed_cleavages, digestion_table_name))

        # Get the table names (including many-to-many table name)
        digestion_tables = self._digestion_tables(enzyme, missed_cleavages)

        # Creates all the tables needed to store the digestion result
        with self._connection:
            try:
                self._connection.execute(f'''CREATE TABLE {digestion_tables.peptides_table}(
                                             id INTEGER,
                                             sequence TEXT NOT NULL UNIQUE,
                                             missed_cleavages INTEGER NOT NULL,
                                             PRIMARY KEY(id))''')

                self._connection.execute(f'''CREATE TABLE {digestion_tables.peptides_association}(
                                             peptide_id INTEGER,
                                             sequence_id INTEGER,
                                             FOREIGN KEY(peptide_id) REFERENCES {digestion_tables.peptides_table}(id),
                                             FOREIGN KEY(sequence_id) REFERENCES sequences(id))''')

                self._digest(enzyme, missed_cleavages, callback=callback, proteins_per_batch=proteins_per_batch)

            except sqlite3.OperationalError:
                self._connection.rollback()
            finally:
                self._end_of_task()

    def _digest(self, enzyme, missed_cleavages, callback=None, proteins_per_batch=10000):
        digestion_tables = self._digestion_tables(enzyme, missed_cleavages)

        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Determining number of sequences to digest...'

        # Counting the number of sequence to digest
        cursor = self._connection.execute(f'''SELECT COUNT(*) FROM sequences WHERE sequences.id NOT IN
                                              (SELECT DISTINCT {digestion_tables.peptides_association}.sequence_id 
                                               FROM {digestion_tables.peptides_association})''')

        self._maximum_task_iteration = cursor.fetchone()[0]
        self._current_task_iteration = 0
        self._current_task = f'''Digesting database with {enzyme}, {missed_cleavages} missed cleavage
                                 {"s" if missed_cleavages > 1 else ""}...'''

        # Nothing to digest, exiting
        if not self._maximum_task_iteration:
            self._end_of_task()
            return

        read_cursor = self._connection.execute(f'''SELECT id, sequence FROM sequences WHERE sequences.id NOT IN
                                                   (SELECT DISTINCT {digestion_tables.peptides_association}.sequence_id 
                                                    FROM {digestion_tables.peptides_association})''')

        rows = read_cursor.fetchmany(proteins_per_batch)
        cleave_function = digester.cleave

        while rows:
            results = ((row[0], cleave_function(row[1], enzyme, missed_cleavages)) for row in rows)

            for (sequence_id, peptides) in results:
                self._connection.executemany(f'''INSERT INTO {digestion_tables.peptides_table}
                                                 (sequence, missed_cleavages) 
                                                 VALUES(?, ?) ON CONFLICT DO NOTHING''',
                                             peptides)

                # Used to map a peptide sequence to its database id
                # We need that to preserve the digestion order of peptide when updating the association table
                peptides_with_id = {}

                for i in range(0, len(peptides), 900):
                    queried_peptides = tuple(peptide[0] for peptide in peptides[i:i + 900])
                    parameters_substitution = ','.join(('?',) * len(queried_peptides))

                    cursor = self._connection.execute(f'''SELECT id, sequence FROM {digestion_tables.peptides_table}
                                                          WHERE sequence IN ({parameters_substitution})''',
                                                      queried_peptides)

                    # Mapping peptide sequence to its id
                    peptides_with_id.update({row['sequence']: row['id'] for row in cursor})

                # Creating a list of ids, sorted by digestion order
                sorted_peptides_id = (peptides_with_id[peptide[0]] for peptide in peptides)

                self._connection.executemany(f'''INSERT INTO {digestion_tables.peptides_association}
                                                 (peptide_id, sequence_id) VALUES(?, ?)''',
                                             ((peptide_id, sequence_id) for peptide_id in sorted_peptides_id))

                self._current_task_iteration += 1
            rows = read_cursor.fetchmany(proteins_per_batch)

    def remove_digestion(self, enzyme: str, missed_cleavages: int, callback: Optional[Callable] = None) -> None:
        self._progress_handler_function = callback
        self._current_task_iteration = 0
        self._maximum_task_iteration = 0
        self._current_task = 'Removing digestion...'
        digestion_tables = self._digestion_tables(enzyme, missed_cleavages)

        with self._connection:
            # self._digestion_tables returns table names surrounded by ", we need to remove them in this case
            self._connection.execute('DELETE FROM digestions WHERE peptides_table = ?',
                                     (digestion_tables.peptides_table[1:-1],))
            self._connection.execute(f'DROP TABLE {digestion_tables.peptides_table}')
            self._connection.execute(f'DROP TABLE {digestion_tables.peptides_association}')

        # VACUUM command is issued to shrink the database
        self._connection.execute('VACUUM')
        self._end_of_task()

    def search_proteins_by_name(self,
                                name: str,
                                limit: Optional[int] = None,
                                callback=None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._current_task_iteration = 0
        self._maximum_task_iteration = 0
        self._current_task = 'Searching proteins by name...'

        sql = f'''SELECT proteins.id, proteins.name, sequences.sequence FROM proteins
                  INNER JOIN sequences ON sequences.id = proteins.sequence_id
                  WHERE proteins.name LIKE ? ORDER BY proteins.name'''

        try:
            cursor = self._connection.execute(sql, ('%' + name.strip() + '%',))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['id'], row['name'], row['sequence'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()

    def search_proteins_by_sequence(self,
                                    sequence: str,
                                    limit: Optional[int] = None,
                                    callback: Optional[Callable] = None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching proteins by sequence...'

        sql = f'''SELECT proteins.id, proteins.name, sequences.sequence FROM proteins
                  INNER JOIN sequences ON sequences.id = proteins.sequence_id
                  WHERE sequences.sequence LIKE ? ORDER BY proteins.name'''

        try:
            cursor = self._connection.execute(sql, ('%' + sequence.strip().upper() + '%',))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['id'], row['name'], row['sequence'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()

    def search_proteins_by_peptide_id(self,
                                      peptide_id: int,
                                      enzyme: str,
                                      missed_cleavages: int,
                                      limit:Optional[int]=None,
                                      callback: Optional[Callable] = None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching proteins by peptide...'
        digestion_tables = self._digestion_tables(enzyme, missed_cleavages)

        sql = f'''SELECT proteins.id, proteins.name, sequences.sequence FROM {digestion_tables.peptides_association}
                  INNER JOIN sequences ON sequences.id = {digestion_tables.peptides_association}.sequence_id
                  INNER JOIN proteins ON proteins.sequence_id = {digestion_tables.peptides_association}.sequence_id
                  WHERE {digestion_tables.peptides_association}.peptide_id = ? ORDER BY proteins.name'''

        try:
            cursor = self._connection.execute(sql, (peptide_id,))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['id'], row['name'], row['sequence'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()

    def search_proteins_by_peptide_sequence(self,
                                            peptide_sequence: str,
                                            enzyme: str,
                                            missed_cleavages: int,
                                            limit:Optional[int]=None,
                                            callback: Optional[Callable] = None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching proteins by peptide...'
        digestion_tables = self._digestion_tables(enzyme, missed_cleavages)

        sql = f'''SELECT proteins.id, proteins.name, sequences.sequence FROM {digestion_tables.peptides_table}
                  INNER JOIN {digestion_tables.peptides_association} ON 
                  {digestion_tables.peptides_association}.peptide_id = {digestion_tables.peptides_table}.id
                  INNER JOIN sequences ON sequences.id = {digestion_tables.peptides_association}.sequence_id
                  INNER JOIN proteins ON proteins.sequence_id = {digestion_tables.peptides_association}.sequence_id
                  WHERE {digestion_tables.peptides_table}.sequence = ? ORDER BY proteins.name'''

        try:
            cursor = self._connection.execute(sql, (peptide_sequence.strip().upper(),))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['id'], row['name'], row['sequence'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()

    def search_peptides_by_protein_id(self,
                                      protein_id: int,
                                      enzyme: str,
                                      missed_cleavages: int,
                                      limit: Optional[int] = None,
                                      callback: Optional[Callable] = None) -> Optional[Iterator[Peptide]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching peptides by protein...'
        digestion_tables = self._digestion_tables(enzyme, missed_cleavages)

        sql = f'''SELECT {digestion_tables.peptides_table}.id, {digestion_tables.peptides_table}.sequence,
                  {digestion_tables.peptides_table}.missed_cleavages, NOT EXISTS(
                  SELECT 1 FROM {digestion_tables.peptides_association}
                  WHERE {digestion_tables.peptides_association}.peptide_id = {digestion_tables.peptides_table}.id AND
                  {digestion_tables.peptides_association}.sequence_id != proteins.sequence_id) AS is_unique FROM proteins
                  INNER JOIN {digestion_tables.peptides_association} ON 
                  {digestion_tables.peptides_association}.sequence_id = proteins.sequence_id
                  INNER JOIN {digestion_tables.peptides_table} ON 
                  {digestion_tables.peptides_table}.id = {digestion_tables.peptides_association}.peptide_id 
                  WHERE proteins.id = ? 
                  ORDER BY {digestion_tables.peptides_association}.rowid'''

        try:
            cursor = self._connection.execute(sql, (protein_id,))
            for i, row in enumerate(cursor, start=1):
                yield Peptide(row['id'], row['sequence'], row['missed_cleavages'], bool(row['is_unique']))

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()
