from pathlib import Path
from typing import MutableMapping, Iterable, TypeVar, Optional

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QFileDialog, QCheckBox, QWidget, QMessageBox

T = TypeVar('T')

_dismissed_error_messages = {}
_dismissed_information_messages = {}
_dismissed_question_messages = {}


def _dismissableMessage(parent: QWidget,
                        message: str,
                        icon: QIcon,
                        buttons: QMessageBox.StandardButton,
                        dismissed_messages: MutableMapping[
                            str, QMessageBox.StandardButton]) -> QMessageBox.StandardButton:
    if message in dismissed_messages:
        return dismissed_messages[message]

    message_box = QMessageBox(icon, 'Protein Digester', message, buttons, parent)
    checkbox = QCheckBox(message_box)
    checkbox.setText('Don\'t warn again')
    message_box.setCheckBox(checkbox)
    button = message_box.exec()

    if checkbox.isChecked():
        dismissed_messages[message] = button

    return button


def resetDismissedMessages() -> None:
    _dismissed_error_messages.clear()
    _dismissed_information_messages.clear()
    _dismissed_question_messages.clear()


def errorMessage(parent: QWidget, message: str, dismissable: bool = False) -> None:
    if dismissable:
        _dismissableMessage(parent,
                            message,
                            QMessageBox.Critical,
                            QMessageBox.Ok,
                            _dismissed_error_messages)
    else:
        QMessageBox.critical(parent, 'Protein Digester', message)


def informationMessage(parent: QWidget, message: str, dismissable: bool = False) -> None:
    if dismissable:
        _dismissableMessage(parent, message, QMessageBox.Information, QMessageBox.Ok, _dismissed_information_messages)
    else:
        QMessageBox.information(parent, 'Protein Digester', message)


def questionMessage(parent: QWidget, message: str, dismissable: bool = False) -> bool:
    if dismissable:
        button = _dismissableMessage(parent,
                                     message,
                                     QMessageBox.Question,
                                     QMessageBox.Yes | QMessageBox.No,
                                     _dismissed_question_messages)
    else:
        button = QMessageBox.question(parent, 'Protein Digester', message)

    return button == QMessageBox.Yes


def detailedErrorMessage(parent: QWidget, message: str, detailedInformation: str) -> None:
    message_box = QMessageBox(QMessageBox.Critical,
                              'Protein Digester',
                              message,
                              QMessageBox.Ok,
                              parent)
    message_box.setDetailedText(detailedInformation)
    message_box.exec()


def choiceDialog(parent: QWidget,
                 message: str,
                 labels: Iterable[str],
                 choices: Iterable[T],
                 show_cancel_button=True) -> T:
    buttons_to_choices = {}
    message_box = QMessageBox(QMessageBox.Question, 'Protein Digester', message, QMessageBox.NoButton, parent)

    for label, choice in zip(labels, choices):
        button = message_box.addButton(label, QMessageBox.ActionRole)
        buttons_to_choices[button] = choice

    if show_cancel_button:
        button = message_box.addButton(QMessageBox.Cancel)
        buttons_to_choices[button] = None

    message_box.exec()
    return buttons_to_choices[message_box.clickedButton()]


def fileOpenDialog(parent: QWidget, title: str, folder: str = '', filter: str = '') -> Path:
    path = QFileDialog.getOpenFileName(parent, title, folder, filter)[0]
    return Path(path) if path else None


def fileSaveDialog(parent: QWidget,
                   title: str,
                   folder: str = '',
                   filter: str = '',
                   extension: str = '') -> Optional[Path]:
    path = QFileDialog.getSaveFileName(parent, title, folder, filter)[0]

    if not path:
        return None

    if not path.endswith('.' + extension):
        path += '.' + extension

    return Path(path)


def folderOpenDialog(parent: QWidget, title: str, folder: str = '') -> Path:
    path = QFileDialog.getExistingDirectory(parent, title, folder, QFileDialog.ShowDirsOnly)
    return Path(path) if path else None
