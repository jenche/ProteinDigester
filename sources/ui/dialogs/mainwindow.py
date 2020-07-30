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

from enum import IntEnum
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import (QApplication, QLabel, QProgressDialog, QTableWidgetItem, QHeaderView, QAction,
                               QActionGroup, QMessageBox, QMainWindow)

from digestiondatabase.digestiondatabase import DigestionDatabase, ResultsLimitExceededError
from ui.autogenerated.mainwindow import Ui_MainWindow
from ui.dialogs import commondialog
from ui.dialogs.digestiondialog import DigestionDialog


class TableItemDataRole(IntEnum):
    ROW_OBJECT = Qt.UserRole


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # Setting status bar
        self.statusLabel = QLabel()
        self.statusLabel.setContentsMargins(6, 0, 0, 6)
        self.statusBar.addWidget(self.statusLabel)

        # Set tables widget resizing policy
        header = self.proteinsTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        header = self.peptidesTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        header = self.subProteinsTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # Variable holding the currently opened database
        self._database: Optional[DigestionDatabase] = None

        # Creating dialogs
        self._progress_dialog = QProgressDialog(self)
        self._progress_dialog.setWindowModality(Qt.WindowModal)
        self._progress_dialog.setMinimumDuration(200)
        self._progress_dialog.reset()

        # Creating an action group used in the working digestion menu
        self._working_digestion_action_group = QActionGroup(self.workingDigestionMenu)
        self._working_digestion_action_group.triggered.connect(self.workingDigestionMenuActionTriggered)

        # First refresh
        self.refreshMenusButtonsStatusBar()

    @property
    def database(self) -> DigestionDatabase:
        return self._database

    def _progressCallback(self, task: str, iteration: int, maximum: int) -> bool:
        if iteration == -1:
            self._progress_dialog.close()
            self._progress_dialog.reset()
            return False
        else:
            self._progress_dialog.setLabelText(task)
            self._progress_dialog.setMaximum(maximum)
            self._progress_dialog.setValue(iteration)

            if not iteration:
                QApplication.processEvents()

            return self._progress_dialog.wasCanceled()

    def refreshMenusButtonsStatusBar(self, reset: bool = False) -> None:
        if not self._database:
            self.statusLabel.setText('No database opened')
        else:
            protein = f'{self._database.proteins_count} protein{"s" if self._database.proteins_count > 1 else ""}'
            sequence = f'{self._database.sequences_count} sequence{"s" if self._database.sequences_count > 1 else ""}'
            self.statusLabel.setText(', '.join((str(self._database.path), protein, sequence)))

        if reset:
            self.proteinsSearchLineEdit.setText('')
            self.proteinsTableWidget.setRowCount(0)

        database_opened = bool(self._database)
        digestions_available = database_opened and bool(self._database.available_digestions)
        database_is_coherent = database_opened and bool(self._database.is_coherent_with_enzymes_collection)
        self.mainSplitter.setEnabled(database_opened)
        self.mainSplitterBottomWidget.setVisible(digestions_available)
        self.databaseMenu.setEnabled(database_opened and database_is_coherent)
        self.workingDigestionMenu.setEnabled(digestions_available)

        if digestions_available:
            if self._working_digestion_action_group.actions():
                current_digestion_settings = self._working_digestion_action_group.checkedAction().data()
            else:
                current_digestion_settings = None

            new_digestion_settings = None

            for action in self._working_digestion_action_group.actions():
                self._working_digestion_action_group.removeAction(action)
                action.deleteLater()

            for i, digestion in enumerate(self.database.available_digestions):
                action_title = (f'{digestion.enzyme} - {digestion.missed_cleavages} missed cleavage'
                                f'{"s" if digestion.missed_cleavages > 1 else ""}')

                # Adding action to working digestion menu
                action = QAction(action_title, self._working_digestion_action_group)
                action.setCheckable(True)
                action.setData(digestion)
                self.workingDigestionMenu.addAction(action)

                if digestion == current_digestion_settings or not i:
                    new_digestion_settings = digestion
                    action.setChecked(True)

            # Refreshing if needed
            if current_digestion_settings != new_digestion_settings:
                self.refreshPeptidesTableWidget()

    def refreshProteinsTableWidget(self) -> None:
        search_text = self.proteinsSearchLineEdit.text().strip()

        if not search_text:
            return

        search_mode = self.proteinsSearchTypeComboBox.currentIndex()

        if search_mode == 0:
            results = self._database.search_proteins_by_name(search_text,
                                                             limit=10000,
                                                             callback=self._progressCallback)
        elif search_mode == 1:
            results = self._database.search_proteins_by_sequence(search_text,
                                                                 limit=10000,
                                                                 callback=self._progressCallback)
        elif search_mode == 2:
            digestion_settings = self._working_digestion_action_group.checkedAction().data()
            results = self._database.search_proteins_by_peptide_sequence(search_text,
                                                                         digestion_settings,
                                                                         limit=10000,
                                                                         callback=self._progressCallback)
        else:
            raise ValueError

        self.proteinsTableWidget.setRowCount(0)
        self.proteinsTableWidget.setSortingEnabled(False)

        try:
            for i, protein in enumerate(results):
                self.proteinsTableWidget.insertRow(i)
                index_item = QTableWidgetItem(str(i + 1).zfill(5))
                index_item.setData(TableItemDataRole.ROW_OBJECT, protein)
                name_item = QTableWidgetItem(protein.name)
                self.proteinsTableWidget.setItem(i, 0, index_item)
                self.proteinsTableWidget.setItem(i, 1, name_item)

        except ResultsLimitExceededError:
            commondialog.informationMessage(self,
                                            'Your search returns too much results.\n'
                                            'Only the 10000 first results will be displayed.',
                                            dismissable=True)

        self.proteinsTableWidget.setSortingEnabled(True)
        self.proteinsTableWidget.resizeColumnToContents(-1)

        # Change search line edit text color to assure the user the search is done
        palette = self.proteinsSearchLineEdit.palette()

        if self.proteinsTableWidget.rowCount():
            palette.setColor(QPalette.Text, QColor(0, 180, 0))
        else:
            palette.setColor(QPalette.Text, QColor(180, 0, 0))

        self.proteinsSearchLineEdit.setPalette(palette)

    def refreshPeptidesTableWidget(self) -> None:
        selected_items = self.proteinsTableWidget.selectedItems()
        selected_protein = selected_items[0].data(TableItemDataRole.ROW_OBJECT) if selected_items else None
        selected_protein_id = selected_protein.id if selected_protein else None
        digestion_settings = self._working_digestion_action_group.checkedAction().data()

        if selected_protein_id and digestion_settings:
            results = self.database.search_peptides_by_protein_id(selected_protein_id,
                                                                  digestion_settings,
                                                                  limit=10000,
                                                                  callback=self._progressCallback)
        else:
            results = []

        self.peptidesTableWidget.setRowCount(0)
        self.peptidesTableWidget.setSortingEnabled(False)

        try:
            for i, peptide in enumerate(results):
                self.peptidesTableWidget.insertRow(i)
                index_item = QTableWidgetItem(str(i + 1).zfill(5))
                index_item.setData(TableItemDataRole.ROW_OBJECT, peptide)
                sequence_item = QTableWidgetItem(peptide.sequence)
                missed_cleavages_item = QTableWidgetItem(str(peptide.missed_cleavages))
                digest_unique_item = QTableWidgetItem('Yes' if peptide.digest_unique else 'No')
                sequence_unique_item = QTableWidgetItem('Yes' if peptide.sequence_unique else 'No')
                self.peptidesTableWidget.setItem(i, 0, index_item)
                self.peptidesTableWidget.setItem(i, 1, sequence_item)
                self.peptidesTableWidget.setItem(i, 2, missed_cleavages_item)
                self.peptidesTableWidget.setItem(i, 3, digest_unique_item)
                self.peptidesTableWidget.setItem(i, 4, sequence_unique_item)

        except ResultsLimitExceededError:
            commondialog.informationMessage(self,
                                            'Your search returns too much results.\n'
                                            'Only the 10000 first results will be displayed.',
                                            dismissable=True)

        self.peptidesTableWidget.setSortingEnabled(True)
        self.proteinsTableWidget.resizeColumnToContents(-1)

    def refreshSubProteinsTableWidget(self) -> None:
        selected_items = self.peptidesTableWidget.selectedItems()
        selected_peptide = selected_items[0].data(TableItemDataRole.ROW_OBJECT) if selected_items else None
        selected_peptide_id = selected_peptide.id if selected_peptide else None
        selected_peptide_sequence = selected_peptide.sequence if selected_peptide else None
        digestion_settings = self._working_digestion_action_group.checkedAction().data()
        by_id_results_ids_set = set()
        limit_reached = False

        self.subProteinsTableWidget.setRowCount(0)
        self.subProteinsTableWidget.setSortingEnabled(False)

        if selected_peptide_id:
            by_id_results = self.database.search_proteins_by_peptide_id(selected_peptide_id,
                                                                        digestion_settings,
                                                                        limit=10000,
                                                                        callback=self._progressCallback)
        else:
            by_id_results = []

        try:
            for i, protein in enumerate(by_id_results):
                self.subProteinsTableWidget.insertRow(i)
                index_item = QTableWidgetItem(str(i + 1).zfill(5))
                index_item.setData(TableItemDataRole.ROW_OBJECT, protein)
                name_item = QTableWidgetItem(protein.name)
                origin_item = QTableWidgetItem('by digest')
                self.subProteinsTableWidget.setItem(i, 0, index_item)
                self.subProteinsTableWidget.setItem(i, 1, name_item)
                self.subProteinsTableWidget.setItem(i, 2, origin_item)
                by_id_results_ids_set.add(protein.id)

        except ResultsLimitExceededError:
            commondialog.informationMessage(self,
                                            'Your search returns too much results.\n'
                                            'Only the 10000 first results will be displayed.',
                                            dismissable=True)
            limit_reached = True

        if selected_peptide_sequence and not limit_reached:
            by_sequence_results = self.database.search_proteins_by_sequence(selected_peptide_sequence,
                                                                            limit=10000,
                                                                            callback=self._progressCallback)
        else:
            by_sequence_results = []

        try:
            for i, protein in enumerate((filtered_protein for filtered_protein in by_sequence_results if
                                         filtered_protein.id not in by_id_results_ids_set),
                                        start=len(by_id_results_ids_set)):
                self.subProteinsTableWidget.insertRow(i)
                index_item = QTableWidgetItem(str(i + 1).zfill(5))
                index_item.setData(TableItemDataRole.ROW_OBJECT, protein)
                name_item = QTableWidgetItem(protein.name)
                origin_item = QTableWidgetItem('by sequence')
                self.subProteinsTableWidget.setItem(i, 0, index_item)
                self.subProteinsTableWidget.setItem(i, 1, name_item)
                self.subProteinsTableWidget.setItem(i, 2, origin_item)

        except ResultsLimitExceededError:
            commondialog.informationMessage(self,
                                            'Your search returns too much by_id_results.\n'
                                            'Only the 10000 first results will be displayed.',
                                            dismissable=True)

        self.subProteinsTableWidget.setSortingEnabled(True)
        self.subProteinsTableWidget.resizeColumnToContents(-1)

    def createDatabaseActionTriggered(self) -> None:
        database_path = commondialog.fileSaveDialog(self,
                                                    'Creating a database',
                                                    filter='Digest database (*.digestdb)',
                                                    extension='digestdb')

        if database_path:
            if self._database:
                self._database.close()

            self._database = DigestionDatabase(database_path, True, True)

        self.refreshMenusButtonsStatusBar(reset=True)

    def openDatabaseActionTriggered(self) -> None:
        database_path = commondialog.fileOpenDialog(self, 'Loading a database', filter='Digest database (*.digestdb)')

        if not database_path:
            return

        if self._database:
            self._database.close()

        self._database = DigestionDatabase(database_path)

        if not self._database.is_coherent_with_enzymes_collection:
            commondialog.informationMessage(self, 'This database includes digestions done with enzymes that have '
                                                  'been removed or modified in the enzymes files.\n'
                                                  'Since this can lead to incoherent results, the import FASTA and '
                                                  'manage database functions will be disabled.')

        self.refreshMenusButtonsStatusBar(reset=True)

    def importFastaActionTriggered(self) -> None:
        fasta_path = commondialog.fileOpenDialog(self, 'Importing a FASTA file', filter='FASTA database(*.fasta)')

        if fasta_path:
            self._database.import_database(fasta_path, callback=self._progressCallback)
            self.refreshMenusButtonsStatusBar()

    def manageDigestionActionTriggered(self) -> None:
        digestion_settings = DigestionDialog(self).run(self._database)

        if digestion_settings is not None:
            self._database.update_digestion(digestion_settings, remove=True, callback=self._progressCallback)
            self.refreshMenusButtonsStatusBar()

    def removeDigestionMenuActionTriggered(self, action) -> None:
        digestion = action.data()
        if commondialog.questionMessage(self,
                                        f'Are you sure you want to remove the digestion '
                                        f'{digestion.enzyme} - {digestion.missed_cleavages} missed cleavages'
                                        f'{"s" if digestion.missed_cleavages > 1 else ""} ?'):
            self._database.remove_digestion(digestion, self._progressCallback)
            self.refreshMenusButtonsStatusBar()

    def workingDigestionMenuActionTriggered(self, action) -> None:
        self.refreshPeptidesTableWidget()

    def proteinsSearchLineEditTextChanged(self, text):
        # Sets back text to standard color (in case it was set to red)
        self.proteinsSearchLineEdit.setPalette(QApplication.style().standardPalette())

    def proteinsSearchPushButtonClicked(self) -> None:
        self.refreshProteinsTableWidget()

    def proteinsTableWidgetItemSelectionChanged(self) -> None:
        self.peptidesTableWidget.setRowCount(0)

    def peptidesTableWidgetItemSelectionChanged(self) -> None:
        self.subProteinsTableWidget.setRowCount(0)

    def aboutActionTriggered(self) -> None:
        QMessageBox.about(self,
                          'About',
                          f'{QApplication.applicationName()} {QApplication.applicationVersion()}')
