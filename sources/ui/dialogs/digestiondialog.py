from typing import Optional, Set

from PySide2.QtWidgets import QDialog, QWidget, QTableWidgetItem, QHeaderView
from PySide2.QtGui import QColor

from digestiondatabase import enzymescollection
from digestiondatabase.digestiondatabase import DigestionDatabase, DigestionSettings
from ui import uibuilder
from ui.dialogs import commondialog

class DigestionDialog(*uibuilder.loadUiType('../ui/digestiondialog.ui')):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setupUi(self)

        # Set tables widget resizing policy
        header = self.digestionSettingsTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def _generateDigestionSettings(self):
        digestion_settings = set()

        for i in range(self.digestionSettingsTableWidget.rowCount()):
            enzyme_item = self.digestionSettingsTableWidget.item(i, 0)
            missed_cleavages_item = self.digestionSettingsTableWidget.item(i, 1)
            enzyme = enzyme_item.text()
            missed_cleavages = int(missed_cleavages_item.text())
            digestion_settings.add(DigestionSettings(enzyme, missed_cleavages))

        return digestion_settings

    def enzymeComboBoxCurrentTextChanged(self, text: str) -> None:
        try:
            enzyme = enzymescollection.enzyme(text)
        except enzymescollection.InvalidEnzymeError:
            self.enzymeDescriptionLabel.setText('')
        else:
            self.enzymeDescriptionLabel.setText(f'<i>{enzyme.name}: {enzyme.description}</i>')

    def addPushButtonClicked(self):
        digestion_settings = DigestionSettings(self.enzymeComboBox.currentText(), self.missedCleavagesSpinBox.value())

        if not digestion_settings in self._generateDigestionSettings():
            row = self.digestionSettingsTableWidget.rowCount()
            self.digestionSettingsTableWidget.insertRow(row)
            enzyme_item = QTableWidgetItem(self.enzymeComboBox.currentText())
            missed_cleavages_item = QTableWidgetItem(str(self.missedCleavagesSpinBox.value()))
            rule_item = QTableWidgetItem(enzymescollection.enzyme(self.enzymeComboBox.currentText()).description)
            self.digestionSettingsTableWidget.setItem(row, 0, enzyme_item)
            self.digestionSettingsTableWidget.setItem(row, 1, missed_cleavages_item)
            self.digestionSettingsTableWidget.setItem(row, 2, rule_item)
            self.digestionSettingsTableWidget.selectRow(row)
        else:
            commondialog.errorMessage(self, 'This digestion settings is already listed.')

    def removePushButtonClicked(self):
        selected_items = self.digestionSettingsTableWidget.selectedItems()
        selected_row = self.digestionSettingsTableWidget.row(selected_items[0])
        self.digestionSettingsTableWidget.removeRow(selected_row)

    def digestionSettingsTableWidgetItemSelectionChanged(self):
        selected_items = self.digestionSettingsTableWidget.selectedItems()
        self.removePushButton.setEnabled(bool(selected_items))

        if selected_items:
            selected_row = self.digestionSettingsTableWidget.row(selected_items[0])
            enzyme_item = self.digestionSettingsTableWidget.item(selected_row, 0)
            missed_cleavages_item = self.digestionSettingsTableWidget.item(selected_row, 1)
            self.enzymeComboBox.setCurrentText(enzyme_item.text())
            self.missedCleavagesSpinBox.setValue(int(missed_cleavages_item.text()))

    def run(self, database: DigestionDatabase) -> Optional[Set[DigestionSettings]]:
        # Refreshing anzymes combobox
        self.enzymeComboBox.clear()

        for enzyme in enzymescollection.available_enzymes():
            self.enzymeComboBox.addItem(enzyme)

        # Refreshing digestion settings table
        self.digestionSettingsTableWidget.setRowCount(0)
        self.digestionSettingsTableWidget.setSortingEnabled(False)

        for i, digestion in enumerate(database.available_digestions):
            self.digestionSettingsTableWidget.insertRow(i)
            enzyme_item = QTableWidgetItem(digestion.enzyme)
            missed_cleavages_item = QTableWidgetItem(str(digestion.missed_cleavages))
            rule_item = QTableWidgetItem(enzymescollection.enzyme(digestion.enzyme).description)
            self.digestionSettingsTableWidget.setItem(i, 0, enzyme_item)
            self.digestionSettingsTableWidget.setItem(i, 1, missed_cleavages_item)
            self.digestionSettingsTableWidget.setItem(i, 2, rule_item)

        self.digestionSettingsTableWidget.setSortingEnabled(True)

        if self.exec() == QDialog.Accepted:
            return self._generateDigestionSettings()

        return None
