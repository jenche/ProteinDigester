#  ProteinDigester
#      Copyright (C) 2020  Julien ENCHE
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sqlite3
import uuid
from collections import namedtuple
from pathlib import Path
from time import time
from typing import Tuple, Union, Iterator, Callable, Optional, Iterable

from digestiondatabase import enzymescollection, fastareader
from .aminoacidsequence import AminoAcidSequence
from .peptide import Peptide
from .protein import Protein

DigestionSettings = namedtuple('DigestionSettings', ('enzyme', 'missed_cleavages'))
DigestionTables = namedtuple('DigestionTables', ('peptides_table', 'peptides_association',
                                                 'peptides_table_index', 'peptides_association_index'))


class DigestionAlreadyExistsError(Exception):
    pass


class DigestionDoesntExistError(Exception):
    pass


class ResultsLimitExceededError(Exception):
    pass


class IncoherencyWithEnzymesCollectionError(Exception):
    pass


class DigestionDatabase:
    def __init__(self, database_path: Union[Path, str], create=False, overwrite=False) -> None:
        self._last_progress_handler_call: Optional[float] = None
        self._current_task_iteration = 0
        self._maximum_task_iteration = 0
        self._current_task = ''
        self._progress_handler_function: Optional[Callable] = None
        self._path = Path(database_path)

        if self._path.exists() and self._path.is_file():
            if create:
                if overwrite:
                    Path(self._path).unlink()
                else:
                    raise FileExistsError
        elif not create:
            raise FileNotFoundError

        try:
            self._connection = sqlite3.connect(str(self._path))
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
                                            rule TEXT NOT NULL,
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
    def is_coherent_with_enzymes_collection(self) -> bool:
        # Checks that the enzymes used in the database still exist in the collections and that the rules used in
        # the database are the same than the ones in the collection
        available_enzymes = enzymescollection.available_enzymes()
        cursor = self._connection.execute('SELECT enzyme, rule FROM digestions')

        for row in cursor:
            if row['enzyme'] not in available_enzymes or row['rule'] != enzymescollection.enzyme(row['enzyme']).rule:
                return False

        return True

    @property
    def path(self) -> Path:
        return self._path

    def _digestion_tables(self, digestion: DigestionSettings) -> DigestionTables:
        if not self._connection:
            raise RuntimeError('No database is opened')

        if digestion not in self.available_digestions:
            raise DigestionDoesntExistError('Digestion doesn\'t exist')

        cursor = self._connection.execute('''SELECT peptides_table FROM digestions 
                                             WHERE enzyme = ? AND missed_cleavages = ?''',
                                          (digestion.enzyme, digestion.missed_cleavages))
        digestion_tables = cursor.fetchone()['peptides_table']
        return DigestionTables(f'"{digestion_tables}"',
                               f'"{digestion_tables + "_association"}"',
                               f'"{digestion_tables + "_index"}"',
                               f'"{digestion_tables + "_association_index"}"')

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

        cursor = self._connection.execute('SELECT id FROM proteins ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        return row['id'] if row else 0

    @property
    def sequences_count(self) -> int:
        if not self._connection:
            raise RuntimeError('No database is opened')

        cursor = self._connection.execute('SELECT id FROM sequences ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        return row['id'] if row else 0

    def import_database(self, filename: Union[Path, str], callback=None) -> None:
        def handle_callback(progress, maximum):
            self._current_task_iteration = progress
            self._maximum_task_iteration = maximum

        if not self._connection:
            raise RuntimeError('No database is opened')

        if not self.is_coherent_with_enzymes_collection:
            raise IncoherencyWithEnzymesCollectionError

        self._current_task = 'Importing FASTA file...'
        self._progress_handler_function = callback

        with self._connection:
            try:
                for i, protein in enumerate(fastareader.read(str(filename), handle_callback), start=1):
                    self._connection.execute('INSERT INTO sequences(sequence) VALUES(?) ON CONFLICT DO NOTHING',
                                             (protein.sequence,))
                    cursor = self._connection.execute('SELECT id FROM sequences WHERE sequence = ?',
                                                      (protein.sequence,))
                    self._connection.execute('''INSERT INTO proteins(name, sequence_id) VALUES(?, ?) ON CONFLICT DO
                                                NOTHING''',
                                             (protein.name, cursor.fetchone()['id']))

                for digestion in self.available_digestions:
                    self._digest(digestion, callback=callback)

            except sqlite3.OperationalError:
                # Callback has returned a non-null value
                self._connection.rollback()
            finally:
                self._end_of_task()

    def update_digestion(self,
                         digestion_settings: Iterable[DigestionSettings],
                         remove=False,
                         callback=None,
                         proteins_per_batch=10000) -> None:
        available_digestions = set(self.available_digestions)
        updated_digestions = set(digestion_settings)
        self._progress_handler_function = callback
        cleanup_needed = False

        if not self.is_coherent_with_enzymes_collection:
            raise IncoherencyWithEnzymesCollectionError

        # Removing unneeded digestions
        if remove:
            self._current_task_iteration = 0
            self._maximum_task_iteration = 0

            with self._connection:
                for digestion in available_digestions - updated_digestions:
                    cleanup_needed = True
                    self._current_task = (f'Removing digestion {digestion.enzyme}, {digestion.missed_cleavages} '
                                          f'missed cleavage{"s" if digestion.missed_cleavages > 1 else ""}...')
                    self._progress_handler()
                    digestion_tables = self._digestion_tables(digestion)

                    try:
                        # self._digestion_tables returns table names surrounded by ", we need to remove them in this
                        # case
                        self._connection.execute('DELETE FROM digestions WHERE peptides_table = ?',
                                                 (digestion_tables.peptides_table[1:-1],))
                        self._connection.execute(f'DROP TABLE {digestion_tables.peptides_table}')
                        self._connection.execute(f'DROP TABLE {digestion_tables.peptides_association}')
                    except sqlite3.OperationalError:
                        self._connection.rollback()
                        self._end_of_task()
                        return

        # Adding digestions
        with self._connection:
            added_digestions = list(updated_digestions - available_digestions)
            added_digestions.sort(key=lambda digestion: digestion.missed_cleavages)
            added_digestions.sort(key=lambda digestion: digestion.enzyme)

            for digestion in added_digestions:
                # Generates a uuid as the table name
                digestion_table_name = uuid.uuid4().hex

                # Add this digestion table into the list of digestion
                enzyme = enzymescollection.enzyme(digestion.enzyme)
                self._connection.execute('''INSERT INTO digestions(enzyme, rule, missed_cleavages, peptides_table)
                                            VALUES(?, ?, ?, ?)''',
                                         (enzyme.name, enzyme.rule, digestion.missed_cleavages, digestion_table_name))

                # Get the table names (including many-to-many table name)
                digestion_tables = self._digestion_tables(digestion)

                # Creates all the tables needed to store the digestion result
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

                    self._digest(digestion, callback=callback, proteins_per_batch=proteins_per_batch)

                except sqlite3.OperationalError:
                    self._connection.rollback()
                    self._end_of_task()
                    return

        if cleanup_needed:
            self._current_task = (f'Cleaning up database...')
            self._connection.execute('VACUUM')

        self._end_of_task()

    def _digest(self, digestion, callback=None, proteins_per_batch=10000) -> None:
        digestion_tables = self._digestion_tables(digestion)
        enzyme = enzymescollection.enzyme(digestion.enzyme)
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Determining number of sequences to digest...'

        # Counting the number of sequence to digest
        cursor = self._connection.execute(f'''SELECT COUNT(*) FROM sequences WHERE sequences.id NOT IN
                                              (SELECT DISTINCT {digestion_tables.peptides_association}.sequence_id 
                                               FROM {digestion_tables.peptides_association})''')

        self._maximum_task_iteration = cursor.fetchone()[0]

        # Nothing to digest, exiting
        if not self._maximum_task_iteration:
            return

        self._current_task_iteration = 0
        self._current_task = (f'Digesting database with {digestion.enzyme}, {digestion.missed_cleavages} '
                              f'missed cleavage{"s" if digestion.missed_cleavages > 1 else ""}...')

        # Dropping the indicies to speed up digestion
        self._connection.execute(f'DROP INDEX IF EXISTS {digestion_tables.peptides_table_index}')
        self._connection.execute(f'DROP INDEX IF EXISTS {digestion_tables.peptides_association_index}')

        # Reading sequences to digest...
        read_cursor = self._connection.execute(f'''SELECT id, sequence FROM sequences WHERE sequences.id NOT IN
                                                   (SELECT DISTINCT {digestion_tables.peptides_association}.sequence_id 
                                                    FROM {digestion_tables.peptides_association})''')

        rows = read_cursor.fetchmany(proteins_per_batch)

        while rows:
            for aa_sequence in (AminoAcidSequence(row['sequence'], row['id']) for row in rows):
                peptides = tuple(enzyme.cleave(aa_sequence, digestion.missed_cleavages))
                self._connection.executemany(f'''INSERT INTO {digestion_tables.peptides_table}
                                                 (sequence, missed_cleavages) 
                                                 VALUES(?, ?) ON CONFLICT DO NOTHING''',
                                             ((peptide.sequence, peptide.missed_cleavages) for peptide in peptides))

                # We need that to preserve the digestion order of peptide when updating the association table
                sequences_to_ids = {}

                for i in range(0, len(peptides), 900):
                    queried_peptide_sequences = tuple(peptide.sequence for peptide in peptides[i:i + 900])
                    parameters_substitution = ','.join(('?',) * len(queried_peptide_sequences))

                    cursor = self._connection.execute(f'''SELECT id, sequence FROM {digestion_tables.peptides_table}
                                                          WHERE sequence IN ({parameters_substitution})''',
                                                      queried_peptide_sequences)

                    # Mapping peptide sequence to its id
                    sequences_to_ids.update({row['sequence']: row['id'] for row in cursor})

                # Creating a list of ids, sorted by digestion order
                sorted_peptides_id = (sequences_to_ids[peptide.sequence] for peptide in peptides)

                self._connection.executemany(f'''INSERT INTO {digestion_tables.peptides_association}
                                                 (peptide_id, sequence_id) VALUES(?, ?)''',
                                             ((peptide_id, aa_sequence.id) for peptide_id in sorted_peptides_id))

                self._current_task_iteration += 1
            rows = read_cursor.fetchmany(proteins_per_batch)

        # Creating indicies to speed up search
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = (f'Creating index for digestion {digestion.enzyme}, {digestion.missed_cleavages} '
                              f'missed cleavage{"s" if digestion.missed_cleavages > 1 else ""}...')
        self._connection.execute(f'''CREATE INDEX {digestion_tables.peptides_table_index} ON  
                                     {digestion_tables.peptides_table}(sequence)''')
        self._connection.execute(f'''CREATE INDEX {digestion_tables.peptides_association_index} ON  
                                     {digestion_tables.peptides_association}(peptide_id, sequence_id)''')

    def search_proteins_by_name(self,
                                name: str,
                                limit: Optional[int] = None,
                                callback=None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._current_task_iteration = 0
        self._maximum_task_iteration = 0
        self._current_task = 'Searching proteins by name...'
        search_terms = {search_term.lower() for search_term in name.split()}

        sql = f'''SELECT proteins.id, proteins.name, sequences.sequence FROM proteins
                  INNER JOIN sequences ON sequences.id = proteins.sequence_id
                  WHERE ''' + ' AND '.join(['proteins.name LIKE ?'] * len(search_terms))

        try:
            cursor = self._connection.execute(sql, tuple('%' + search_term + '%' for search_term in search_terms))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['name'], row['sequence'], protein_id=row['id'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            raise

        self._end_of_task()

    def search_proteins_by_sequence(self,
                                    sequence: str,
                                    limit: Optional[int] = None,
                                    callback: Optional[Callable] = None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching proteins by sequence...'

        sql = '''SELECT proteins.id, proteins.name, sequences.sequence FROM proteins
                 INNER JOIN sequences ON sequences.id = proteins.sequence_id
                 WHERE sequences.sequence LIKE ? ORDER BY proteins.name'''

        try:
            cursor = self._connection.execute(sql, ('%' + sequence.strip().upper() + '%',))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['name'], row['sequence'], protein_id=row['id'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()

    def search_proteins_by_peptide_id(self,
                                      peptide_id: int,
                                      digestion: DigestionSettings,
                                      limit: Optional[int] = None,
                                      callback: Optional[Callable] = None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching proteins by peptide...'
        digestion_tables = self._digestion_tables(digestion)

        sql = f'''SELECT proteins.id, proteins.name, sequences.sequence FROM {digestion_tables.peptides_association}
                  INNER JOIN sequences ON sequences.id = {digestion_tables.peptides_association}.sequence_id
                  INNER JOIN proteins ON proteins.sequence_id = {digestion_tables.peptides_association}.sequence_id
                  WHERE {digestion_tables.peptides_association}.peptide_id = ? ORDER BY proteins.name'''

        try:
            cursor = self._connection.execute(sql, (peptide_id,))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['name'], row['sequence'], protein_id=row['id'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()

    def search_proteins_by_peptide_sequence(self,
                                            peptide_sequence: str,
                                            digestion: DigestionSettings,
                                            limit: Optional[int] = None,
                                            callback: Optional[Callable] = None) -> Optional[Iterator[Protein]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching proteins by peptide...'
        digestion_tables = self._digestion_tables(digestion)

        sql = f'''SELECT proteins.id, proteins.name, sequences.sequence FROM {digestion_tables.peptides_table}
                  INNER JOIN {digestion_tables.peptides_association} ON 
                  {digestion_tables.peptides_association}.peptide_id = {digestion_tables.peptides_table}.id
                  INNER JOIN sequences ON sequences.id = {digestion_tables.peptides_association}.sequence_id
                  INNER JOIN proteins ON proteins.sequence_id = {digestion_tables.peptides_association}.sequence_id
                  WHERE {digestion_tables.peptides_table}.sequence = ? ORDER BY proteins.name'''

        try:
            cursor = self._connection.execute(sql, (peptide_sequence.strip().upper(),))
            for i, row in enumerate(cursor, start=1):
                yield Protein(row['name'], row['sequence'], protein_id=row['id'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()

    def search_peptides_by_protein_id(self,
                                      protein_id: int,
                                      digestion: DigestionSettings,
                                      limit: Optional[int] = None,
                                      callback: Optional[Callable] = None) -> Optional[Iterator[Peptide]]:
        self._progress_handler_function = callback
        self._maximum_task_iteration = 0
        self._current_task_iteration = 0
        self._current_task = 'Searching peptides by protein...'
        digestion_tables = self._digestion_tables(digestion)

        sql = f'''SELECT {digestion_tables.peptides_table}.id, {digestion_tables.peptides_table}.sequence,
                  {digestion_tables.peptides_table}.missed_cleavages, NOT EXISTS(
                  SELECT 1 FROM {digestion_tables.peptides_association}
                  WHERE {digestion_tables.peptides_association}.peptide_id = {digestion_tables.peptides_table}.id AND
                  {digestion_tables.peptides_association}.sequence_id != proteins.sequence_id) AS is_digest_unique,
                  NOT EXISTS(SELECT 1 FROM sequences WHERE {digestion_tables.peptides_association}.sequence_id != sequences.id AND
                  sequences.sequence LIKE '%' || {digestion_tables.peptides_table}.sequence || '%') AS is_sequence_unique
                  FROM proteins
                  INNER JOIN {digestion_tables.peptides_association} ON 
                  {digestion_tables.peptides_association}.sequence_id = proteins.sequence_id
                  INNER JOIN {digestion_tables.peptides_table} ON 
                  {digestion_tables.peptides_table}.id = {digestion_tables.peptides_association}.peptide_id 
                  WHERE proteins.id = ? ORDER BY {digestion_tables.peptides_association}.rowid'''

        try:
            cursor = self._connection.execute(sql, (protein_id,))
            for i, row in enumerate(cursor, start=1):
                yield Peptide(row['sequence'],
                              row['missed_cleavages'],
                              digest_unique=bool(row['is_digest_unique']),
                              sequence_unique=bool(row['is_sequence_unique']),
                              peptide_id=row['id'])

                if limit is not None and i + 1 > limit:
                    self._end_of_task()
                    raise ResultsLimitExceededError
        except sqlite3.OperationalError:
            pass

        self._end_of_task()