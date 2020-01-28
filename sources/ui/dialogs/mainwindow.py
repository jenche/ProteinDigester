from enum import IntEnum
from typing import Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QLabel, QProgressDialog, QTableWidgetItem, QHeaderView, QAction, QActionGroup, QMessageBox

from digestiondatabase.digestiondatabase import (DigestionDatabase, DigestionAlreadyExistsError,
                                                 ResultsLimitExceededError)
from ui import uibuilder
from ui.dialogs import commondialog
from ui.dialogs.digestiondialog import DigestionDialog


class TableItemDataRole(IntEnum):
    ROW_OBJECT_ID = Qt.UserRole


class MainWindow(*uibuilder.loadUiType('../ui/mainwindow.ui')):
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

        header = self.subProteinsTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        # Variable holding the currently opened database
        self._database: Optional[DigestionDatabase] = None

        # Creating dialogs
        self._digestion_dialog = DigestionDialog(self)
        self._progress_dialog = QProgressDialog(self)
        self._progress_dialog.setAutoReset(True)
        self._progress_dialog.setAutoClose(True)
        self._progress_dialog.setWindowModality(Qt.WindowModal)
        self._progress_dialog.setMinimumDuration(200)
        self._progress_dialog.reset()

        # Creating menu that can't be created in QT Designer
        self.removeDigestionMenu = self.databaseMenu.addMenu('Remove digestion')
        self.removeDigestionMenu.triggered.connect(self.removeDigestionMenuActionTriggered)

        # First refresh
        self.refreshMenusButtonsStatusBar()

    @property
    def database(self) -> DigestionDatabase:
        return self._database

    def _progressCallback(self, task: str, iteration: int, maximum: int) -> Optional[bool]:
        if iteration == -1:
            self._progress_dialog.reset()
        else:
            self._progress_dialog.setLabelText(task)
            self._progress_dialog.setMaximum(maximum)
            self._progress_dialog.setValue(iteration)

            if not iteration:
                QGuiApplication.processEvents()

            return self._progress_dialog.wasCanceled()

    def refreshMenusButtonsStatusBar(self) -> None:
        if not self._database:
            self.statusLabel.setText('No database opened')
        else:
            protein = f'{self._database.proteins_count} protein{"s" if self._database.proteins_count > 1 else ""}'
            sequence = f'{self._database.sequences_count} sequence{"s" if self._database.sequences_count > 1 else ""}'
            self.statusLabel.setText(', '.join((str(self._database.path), protein, sequence)))

        database_opened = bool(self._database)
        digestions_available = database_opened and bool(self._database.available_digestions)
        self.mainSplitter.setEnabled(database_opened)
        self.mainSplitterBottomWidget.setVisible(digestions_available)
        self.databaseMenu.setEnabled(database_opened)
        self.workingDigestionMenu.setEnabled(digestions_available)
        self.removeDigestionMenu.setEnabled(digestions_available)

        if digestions_available:
            current_digestion_settings = None
            new_digestion_settings = None

            for action in self.workingDigestionMenu.actions():
                if action.isChecked():
                    current_digestion_settings = action.data()
                    break

            self.removeDigestionMenu.clear()
            self.workingDigestionMenu.clear()
            action_group = QActionGroup(self.workingDigestionMenu)

            for i, digestion in enumerate(self.database.available_digestions):
                action_title = (f'{digestion.enzyme} - {digestion.missed_cleavages} missed cleavage'
                                f'{"s" if digestion.missed_cleavages > 1 else ""}')

                # Adding action to working digestion menu
                action = QAction(action_title, action_group)
                action.setCheckable(True)
                action.setData(digestion)
                self.workingDigestionMenu.addAction(action)

                if digestion == current_digestion_settings or not i:
                    new_digestion_settings = digestion
                    action.setChecked(True)

                # Adding action to remove digestion menu
                action = QAction(action_title, self.removeDigestionMenu)
                action.setData(digestion)
                self.removeDigestionMenu.addAction(action)

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
            for action in self.workingDigestionMenu.actions():
                if action.isChecked():
                    digestion_settings = action.data()
                    break

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
                index_item.setData(TableItemDataRole.ROW_OBJECT_ID, protein.id)
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

    def refreshPeptidesTableWidget(self) -> None:
        selected_items = self.proteinsTableWidget.selectedItems()
        selected_protein_id = selected_items[0].data(TableItemDataRole.ROW_OBJECT_ID) if selected_items else None
        digestion_settings = None

        for action in self.workingDigestionMenu.actions():
            if action.isChecked():
                digestion_settings = action.data()
                break

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
                index_item.setData(TableItemDataRole.ROW_OBJECT_ID, peptide.id)
                sequence_item = QTableWidgetItem(peptide.sequence)
                missed_cleavages_item = QTableWidgetItem(str(peptide.missed_cleavages))
                unique_item = QTableWidgetItem('Yes' if peptide.unique else 'No')
                self.peptidesTableWidget.setItem(i, 0, index_item)
                self.peptidesTableWidget.setItem(i, 1, sequence_item)
                self.peptidesTableWidget.setItem(i, 2, missed_cleavages_item)
                self.peptidesTableWidget.setItem(i, 3, unique_item)

        except ResultsLimitExceededError:
            commondialog.informationMessage(self,
                                            'Your search returns too much results.\n'
                                            'Only the 10000 first results will be displayed.',
                                            dismissable=True)

        self.peptidesTableWidget.setSortingEnabled(True)
        self.proteinsTableWidget.resizeColumnToContents(-1)

    def refreshSubProteinsTableWidget(self) -> None:
        selected_items = self.peptidesTableWidget.selectedItems()
        selected_peptide_id = selected_items[0].data(TableItemDataRole.ROW_OBJECT_ID) if selected_items else None

        for action in self.workingDigestionMenu.actions():
            if action.isChecked():
                digestion_settings = action.data()
                break

        if selected_peptide_id:
            results = self.database.search_proteins_by_peptide_id(selected_peptide_id,
                                                                  digestion_settings,
                                                                  limit=10000,
                                                                  callback=self._progressCallback)
        else:
            results = []

        self.subProteinsTableWidget.setRowCount(0)
        self.subProteinsTableWidget.setSortingEnabled(False)

        try:
            for i, protein in enumerate(results):
                self.subProteinsTableWidget.insertRow(i)
                index_item = QTableWidgetItem(str(i + 1).zfill(5))
                index_item.setData(TableItemDataRole.ROW_OBJECT_ID, protein.id)
                name_item = QTableWidgetItem(protein.name)
                self.subProteinsTableWidget.setItem(i, 0, index_item)
                self.subProteinsTableWidget.setItem(i, 1, name_item)

        except ResultsLimitExceededError:
            commondialog.informationMessage(self,
                                            'Your search returns too much results.\n'
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

        self.refreshMenusButtonsStatusBar()

    def openDatabaseActionTriggered(self) -> None:
        database_path = commondialog.fileOpenDialog(self, 'Loading a database', filter='Digest database (*.digestdb)')

        if not database_path:
            return

        if self._database:
            self._database.close()

        self._database = DigestionDatabase(database_path)
        self.refreshMenusButtonsStatusBar()

    def importFastaActionTriggered(self) -> None:
        fasta_path = commondialog.fileOpenDialog(self, 'Importing a FASTA file', filter='FASTA database(*.fasta)')

        if fasta_path:
            self._database.import_database(fasta_path, callback=self._progressCallback)
            self.refreshMenusButtonsStatusBar()

    def addDigestionActionTriggered(self) -> None:
        digestion_settings = self._digestion_dialog.run()

        if digestion_settings:
            try:
                self._database.add_digestion(digestion_settings, callback=self._progressCallback)
            except DigestionAlreadyExistsError:
                commondialog.errorMessage(self, 'This digestion already exists in the database.')

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
        print('coucou')
        self.refreshPeptidesTableWidget()

    def proteinsSearchPushButtonClicked(self) -> None:
        self.refreshProteinsTableWidget()

    def proteinsTableWidgetItemSelectionChanged(self) -> None:
        self.refreshPeptidesTableWidget()

    def peptidesTableWidgetItemSelectionChanged(self) -> None:
        self.refreshSubProteinsTableWidget()

    def aboutActionTriggered(self) -> None:
        QMessageBox.about(self,
                          'About',
                          f'{QGuiApplication.applicationName()} {QGuiApplication.applicationVersion()}')
