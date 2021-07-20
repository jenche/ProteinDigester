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

from pathlib import Path
from typing import MutableMapping, Iterable, TypeVar, Optional

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QCheckBox, QWidget, QMessageBox, QApplication

T = TypeVar('T')

_dismissed_error_messages = {}
_dismissed_information_messages = {}
_dismissed_question_messages = {}


def _dismissableMessage(parent: Optional[QWidget],
                        message: str,
                        icon: QIcon,
                        buttons: QMessageBox.StandardButton,
                        dismissed_messages: MutableMapping[
                            str, QMessageBox.StandardButton]) -> QMessageBox.StandardButton:
    if message in dismissed_messages:
        return dismissed_messages[message]

    message_box = QMessageBox(icon, QApplication.applicationName(), message, buttons, parent)
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


def errorMessage(parent: Optional[QWidget], message: str, dismissable: bool = False) -> None:
    if dismissable:
        _dismissableMessage(parent,
                            message,
                            QMessageBox.Critical,
                            QMessageBox.Ok,
                            _dismissed_error_messages)
    else:
        QMessageBox.critical(parent, QApplication.applicationName(), message)


def informationMessage(parent: Optional[QWidget], message: str, dismissable: bool = False) -> None:
    if dismissable:
        _dismissableMessage(parent, message, QMessageBox.Information, QMessageBox.Ok, _dismissed_information_messages)
    else:
        QMessageBox.information(parent, QApplication.applicationName(), message)


def questionMessage(parent: Optional[QWidget], message: str, dismissable: bool = False) -> bool:
    if dismissable:
        button = _dismissableMessage(parent,
                                     message,
                                     QMessageBox.Question,
                                     QMessageBox.Yes | QMessageBox.No,
                                     _dismissed_question_messages)
    else:
        button = QMessageBox.question(parent, QApplication.applicationName(), message)

    return button == QMessageBox.Yes


def detailedErrorMessage(parent: Optional[QWidget], message: str, detailedInformation: str) -> None:
    message_box = QMessageBox(QMessageBox.Critical,
                              QApplication.applicationName(),
                              message,
                              QMessageBox.Ok,
                              parent)
    message_box.setDetailedText(detailedInformation)
    message_box.exec()


def choiceDialog(parent: Optional[QWidget],
                 message: str,
                 labels: Iterable[str],
                 choices: Iterable[T],
                 show_cancel_button=True) -> T:
    buttons_to_choices = {}
    message_box = QMessageBox(QMessageBox.Question, QApplication.applicationName(), message, QMessageBox.NoButton, parent)

    for label, choice in zip(labels, choices):
        button = message_box.addButton(label, QMessageBox.ActionRole)
        buttons_to_choices[button] = choice

    if show_cancel_button:
        button = message_box.addButton(QMessageBox.Cancel)
        buttons_to_choices[button] = None

    message_box.exec()
    return buttons_to_choices[message_box.clickedButton()]


def fileOpenDialog(parent: Optional[QWidget], title: str, folder: str = '', filter: str = '') -> Path:
    path = QFileDialog.getOpenFileName(parent, title, folder, filter)[0]
    return Path(path) if path else None


def fileSaveDialog(parent: Optional[QWidget],
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


def folderOpenDialog(parent: Optional[QWidget], title: str, folder: str = '') -> Path:
    path = QFileDialog.getExistingDirectory(parent, title, folder, QFileDialog.ShowDirsOnly)
    return Path(path) if path else None
