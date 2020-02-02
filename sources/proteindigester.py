import sys
import traceback
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QStyle, QDesktopWidget

from ui.dialogs import commondialog
from ui.dialogs.mainwindow import MainWindow
from digestiondatabase import enzymescollection

APP_NAME = 'ProteinDigester'
APP_VERSION = 0.1


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

        # Deactivating the ? button appearing on every windows
        self.setAttribute(Qt.AA_DisableWindowContextHelpButton)

        # Creating the main window
        self._mainwindow = MainWindow()
        self._mainwindow.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                                        Qt.AlignCenter,
                                                        self._mainwindow.size(),
                                                        QDesktopWidget().availableGeometry(self._mainwindow)))
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
            self.exec_()


if __name__ == '__main__':
    application = Application(sys.argv).exec()
