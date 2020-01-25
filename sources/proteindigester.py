import sys
import traceback

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QStyle, QDesktopWidget, QSplashScreen
from ui.dialogs.mainwindow import MainWindow

from ui.dialogs import commondialog
from typing import List
APP_NAME = 'Protein Digester'
APP_VERSION = 1


class Application(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__()
        self._mainwindow = None
        self._debug_mode = False

        self.aboutToQuit.connect(self._uninitialize)
        self.setApplicationVersion(str(APP_VERSION))
        self.setApplicationName(APP_NAME)

        use_gui_exception = True
        show_splash = True

        for arg in argv:
            if arg in ('--stdout-exception', '-e'):
                use_gui_exception = False

            if arg in ('--nosplash', '-n'):
                show_splash = False

        # If --stdout-exception is not passed as argument, exception are shown in a dialog
        if use_gui_exception:
            sys.excepthook = self._exceptionOccured

        # Showing splash screen
        if show_splash:
            splash_screen = QSplashScreen(QPixmap(':/pixmap/splash/splash.png'))
            splash_screen.show()
            self.processEvents()

        # Deactivating the ? button appearing on every windows
        self.setAttribute(Qt.AA_DisableWindowContextHelpButton)

        # Creating the main window
        self._mainwindow = MainWindow()
        self._mainwindow.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                                        Qt.AlignCenter,
                                                        self._mainwindow.size(),
                                                        QDesktopWidget().availableGeometry(self._mainwindow)))

        self._mainwindow.show()

        if show_splash:
            splash_screen.finish(self._mainwindow)

    def _exceptionOccured(self, etype, value, trace) -> None:
        commondialog.detailedErrorMessage(self._mainwindow,
                                          'An unexpected error happened.',
                                          ''.join(traceback.format_exception(etype, value, trace)).strip())

    def _uninitialize(self) -> None:
        if self._mainwindow.database:
            self._mainwindow.database.close()

    def mainWindow(self) -> MainWindow:
        return self._mainwindow


if __name__ == '__main__':
    application = Application(sys.argv).exec_()