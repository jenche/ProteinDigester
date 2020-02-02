from typing import Optional, Iterable

from PySide2.QtCore import QEvent, Qt
from PySide2.QtWidgets import QApplication, QWidget, QTableWidget, QMenu


class TableWidget(QTableWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._context_menu = QMenu(self)
        self._copy_table_action = self._context_menu.addAction('Copy table to clipboard',
                                                               self._copyTableActionTriggered)
        self._copy_row_action = self._context_menu.addAction('Copy row to clipboard',
                                                             self._copyRowActionTriggered)
        self.addActions((self._copy_table_action, self._copy_row_action))

    def contextMenuEvent(self, event: QEvent) -> None:
        self._copy_table_action.setEnabled(bool(self.rowCount()))
        self._copy_row_action.setEnabled(bool(self.selectedItems()))
        self._context_menu.exec_(self.viewport().mapToGlobal(event.pos()))

    def _copyRowsToClipboard(self, rows: Iterable[int]) -> None:
        if not rows or not self.columnCount():
            return

        rows_text = ['\t'.join(self.model().headerData(column, Qt.Horizontal) for column in range(self.columnCount()))]

        for row in rows:
            rows_text.append('\t'.join(self.item(row, column).text() for column in range(self.columnCount())))

        QApplication.clipboard().setText('\n'.join(rows_text))

    def _copyTableActionTriggered(self) -> None:
        self._copyRowsToClipboard(tuple(range(self.rowCount())))

    def _copyRowActionTriggered(self) -> None:
        selected_rows = sorted({self.row(selected_item) for selected_item in self.selectedItems()})
        self._copyRowsToClipboard(selected_rows)
