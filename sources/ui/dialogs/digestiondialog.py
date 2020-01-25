from typing import Optional, Iterable

from PySide2.QtWidgets import QDialog

from digestiondatabase.digestiondatabase import DigestionSettings
from ui import uibuilder


class DigestionDialog(*uibuilder.loadUiType('../ui/digestiondialog.ui')):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)

    def run(self, available_enzymes: Iterable[str]) -> Optional[DigestionSettings]:
        self.enzymeComboBox.clear()
        for enzyme in available_enzymes:
            self.enzymeComboBox.addItem(enzyme)

        if self.exec() == QDialog.Accepted:
            return DigestionSettings(self.enzymeComboBox.currentText(), self.missedCleavagesSpinBox.value())

        return None
