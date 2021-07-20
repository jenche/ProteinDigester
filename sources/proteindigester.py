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

import sys
import traceback
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QStyle

from digestiondatabase import enzymescollection
from ui.dialogs import commondialog
from ui.dialogs.mainwindow import MainWindow

APP_NAME = 'ProteinDigester'
APP_VERSION = 0.3


class Application(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__()
        self._mainwindow = None
        self._debug_mode = False
        self._initialized = False

        self.aboutToQuit.connect(self._uninitialize)
        self.setApplicationVersion(str(APP_VERSION))
        self.setApplicationName(APP_NAME)

        use_gui_exception = True

        for arg in argv:
            if arg in ('--stdout-exception', '-e'):
                use_gui_exception = False

        # If --stdout-exception is not passed as argument, exception are shown in a dialog
        if use_gui_exception:
            sys.excepthook = self._exceptionOccured

        # Creating the main window
        self._mainwindow = MainWindow()
        self._mainwindow.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                                        Qt.AlignCenter,
                                                        self._mainwindow.size(),
                                                        self._mainwindow.screen().availableGeometry()))
        self._mainwindow.show()

        # Loading enzymes
        try:
            enzymescollection.load_from_file('enzymes.ini')
        except FileNotFoundError:
            commondialog.errorMessage(None, 'Enzymes file enzymes.ini was not found.')
        except enzymescollection.InvalidEnzymeFileError as exception:
            commondialog.errorMessage(None, f'File enzymes.ini is invalid.\n{exception}')
        else:
            self._initialized = True

    def _exceptionOccured(self, etype, value, trace) -> None:
        commondialog.detailedErrorMessage(self._mainwindow,
                                          'An unexpected error happened.',
                                          ''.join(traceback.format_exception(etype, value, trace)).strip())

    def _uninitialize(self) -> None:
        if self._mainwindow.database:
            self._mainwindow.database.close()

    def mainWindow(self) -> MainWindow:
        return self._mainwindow

    def exec(self):
        if self._initialized:
            super().exec()


if __name__ == '__main__':
    application = Application(sys.argv).exec()
