from typing import Optional

from PySide2.QtWidgets import QDialog, QWidget

from digestiondatabase import enzymescollection
from digestiondatabase.digestiondatabase import DigestionSettings
from ui import uibuilder


class DigestionDialog(*uibuilder.loadUiType('../ui/digestiondialog.ui')):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setupUi(self)

    def enzymeComboBoxCurrentTextChanged(self, text: str) -> None:
        try:
            enzyme = enzymescollection.enzyme(text)
        except enzymescollection.InvalidEnzymeError:
            self.enzymeDescriptionLabel.setText('')
        else:
            self.enzymeDescriptionLabel.setText(f'<i>{enzyme.name}: {enzyme.description}</i>')

    def run(self) -> Optional[DigestionSettings]:
        self.enzymeComboBox.clear()

        for enzyme in enzymescollection.available_enzymes():
            self.enzymeComboBox.addItem(enzyme)

        if self.exec() == QDialog.Accepted:
            return DigestionSettings(self.enzymeComboBox.currentText(), self.missedCleavagesSpinBox.value())

        return None
