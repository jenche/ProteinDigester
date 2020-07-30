# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject,
                            QRect, QSize, Qt, QLocale)
from PySide2.QtGui import (QIcon)
from PySide2.QtWidgets import *

from ui.widgets.tablewidget import TableWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1223, 689)
        MainWindow.setWindowOpacity(1.000000000000000)
        self.createDatabaseAction = QAction(MainWindow)
        self.createDatabaseAction.setObjectName(u"createDatabaseAction")
        self.openDatabaseAction = QAction(MainWindow)
        self.openDatabaseAction.setObjectName(u"openDatabaseAction")
        self.importFastaAction = QAction(MainWindow)
        self.importFastaAction.setObjectName(u"importFastaAction")
        self.quitAction = QAction(MainWindow)
        self.quitAction.setObjectName(u"quitAction")
        self.manageDigestionAction = QAction(MainWindow)
        self.manageDigestionAction.setObjectName(u"manageDigestionAction")
        self.removeDigestionAction = QAction(MainWindow)
        self.removeDigestionAction.setObjectName(u"removeDigestionAction")
        self.aboutAction = QAction(MainWindow)
        self.aboutAction.setObjectName(u"aboutAction")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.mainSplitter = QSplitter(self.centralwidget)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Vertical)
        self.mainSplitter.setOpaqueResize(True)
        self.mainSplitter.setChildrenCollapsible(False)
        self.mainSplitterTopWidget = QWidget(self.mainSplitter)
        self.mainSplitterTopWidget.setObjectName(u"mainSplitterTopWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.mainSplitterTopWidget.sizePolicy().hasHeightForWidth())
        self.mainSplitterTopWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.mainSplitterTopWidget)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.proteinsTitleLabel = QLabel(self.mainSplitterTopWidget)
        self.proteinsTitleLabel.setObjectName(u"proteinsTitleLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.proteinsTitleLabel.sizePolicy().hasHeightForWidth())
        self.proteinsTitleLabel.setSizePolicy(sizePolicy1)
        self.proteinsTitleLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.proteinsTitleLabel)

        self.proteinsSearchWidget = QWidget(self.mainSplitterTopWidget)
        self.proteinsSearchWidget.setObjectName(u"proteinsSearchWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.proteinsSearchWidget)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.proteinsSearchLineEdit = QLineEdit(self.proteinsSearchWidget)
        self.proteinsSearchLineEdit.setObjectName(u"proteinsSearchLineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.proteinsSearchLineEdit.sizePolicy().hasHeightForWidth())
        self.proteinsSearchLineEdit.setSizePolicy(sizePolicy2)
        self.proteinsSearchLineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_5.addWidget(self.proteinsSearchLineEdit)

        self.proteinsSearchTypeComboBox = QComboBox(self.proteinsSearchWidget)
        self.proteinsSearchTypeComboBox.addItem("")
        self.proteinsSearchTypeComboBox.addItem("")
        self.proteinsSearchTypeComboBox.addItem("")
        self.proteinsSearchTypeComboBox.setObjectName(u"proteinsSearchTypeComboBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.proteinsSearchTypeComboBox.sizePolicy().hasHeightForWidth())
        self.proteinsSearchTypeComboBox.setSizePolicy(sizePolicy3)
        self.proteinsSearchTypeComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.horizontalLayout_5.addWidget(self.proteinsSearchTypeComboBox)

        self.proteinsSearchPushButton = QPushButton(self.proteinsSearchWidget)
        self.proteinsSearchPushButton.setObjectName(u"proteinsSearchPushButton")
        sizePolicy3.setHeightForWidth(self.proteinsSearchPushButton.sizePolicy().hasHeightForWidth())
        self.proteinsSearchPushButton.setSizePolicy(sizePolicy3)
        icon = QIcon()
        icon.addFile(u":/pixmap/icons/16x16/edit-find-symbolic.symbolic.png", QSize(), QIcon.Normal, QIcon.Off)
        self.proteinsSearchPushButton.setIcon(icon)
        self.proteinsSearchPushButton.setIconSize(QSize(16, 16))
        self.proteinsSearchPushButton.setCheckable(False)

        self.horizontalLayout_5.addWidget(self.proteinsSearchPushButton)


        self.verticalLayout_2.addWidget(self.proteinsSearchWidget)

        self.proteinsTableWidget = TableWidget(self.mainSplitterTopWidget)
        if (self.proteinsTableWidget.columnCount() < 2):
            self.proteinsTableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.proteinsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.proteinsTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.proteinsTableWidget.setObjectName(u"proteinsTableWidget")
        self.proteinsTableWidget.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.proteinsTableWidget.setStyleSheet(u"QTableView:!active {selection-color: palette(Highlighted-Text);\n"
                                               "                     selection-background-color: palette(Highlight);}\n"
                                               "                 ")
        self.proteinsTableWidget.setAutoScroll(False)
        self.proteinsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.proteinsTableWidget.setAlternatingRowColors(True)
        self.proteinsTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.proteinsTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.proteinsTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.proteinsTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.proteinsTableWidget.setShowGrid(False)
        self.proteinsTableWidget.setSortingEnabled(True)
        self.proteinsTableWidget.setWordWrap(False)
        self.proteinsTableWidget.setCornerButtonEnabled(False)
        self.proteinsTableWidget.setColumnCount(2)
        self.proteinsTableWidget.horizontalHeader().setStretchLastSection(False)
        self.proteinsTableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.proteinsTableWidget)

        self.mainSplitter.addWidget(self.mainSplitterTopWidget)
        self.mainSplitterBottomWidget = QWidget(self.mainSplitter)
        self.mainSplitterBottomWidget.setObjectName(u"mainSplitterBottomWidget")
        sizePolicy3.setHeightForWidth(self.mainSplitterBottomWidget.sizePolicy().hasHeightForWidth())
        self.mainSplitterBottomWidget.setSizePolicy(sizePolicy3)
        self.verticalLayout_3 = QVBoxLayout(self.mainSplitterBottomWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 6, 0, 0)
        self.splitter = QSplitter(self.mainSplitterBottomWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.subSplitterLeftWidget = QWidget(self.splitter)
        self.subSplitterLeftWidget.setObjectName(u"subSplitterLeftWidget")
        self.verticalLayout = QVBoxLayout(self.subSplitterLeftWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.peptideTitleLabel = QLabel(self.subSplitterLeftWidget)
        self.peptideTitleLabel.setObjectName(u"peptideTitleLabel")
        sizePolicy1.setHeightForWidth(self.peptideTitleLabel.sizePolicy().hasHeightForWidth())
        self.peptideTitleLabel.setSizePolicy(sizePolicy1)
        self.peptideTitleLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.peptideTitleLabel)

        self.peptidesTableWidget = TableWidget(self.subSplitterLeftWidget)
        if (self.peptidesTableWidget.columnCount() < 5):
            self.peptidesTableWidget.setColumnCount(5)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.peptidesTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.peptidesTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.peptidesTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.peptidesTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.peptidesTableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem6)
        self.peptidesTableWidget.setObjectName(u"peptidesTableWidget")
        self.peptidesTableWidget.setStyleSheet(u"QTableView:!active {selection-color: palette(Highlighted-Text);\n"
                                               "                                        selection-background-color: palette(Highlight);}\n"
                                               "                                    ")
        self.peptidesTableWidget.setAutoScroll(False)
        self.peptidesTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.peptidesTableWidget.setAlternatingRowColors(True)
        self.peptidesTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.peptidesTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.peptidesTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.peptidesTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.peptidesTableWidget.setShowGrid(False)
        self.peptidesTableWidget.setSortingEnabled(True)
        self.peptidesTableWidget.setWordWrap(False)
        self.peptidesTableWidget.setCornerButtonEnabled(False)
        self.peptidesTableWidget.horizontalHeader().setStretchLastSection(False)
        self.peptidesTableWidget.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.peptidesTableWidget)

        self.splitter.addWidget(self.subSplitterLeftWidget)
        self.subSplitterRightWidget = QWidget(self.splitter)
        self.subSplitterRightWidget.setObjectName(u"subSplitterRightWidget")
        sizePolicy3.setHeightForWidth(self.subSplitterRightWidget.sizePolicy().hasHeightForWidth())
        self.subSplitterRightWidget.setSizePolicy(sizePolicy3)
        self.verticalLayout_5 = QVBoxLayout(self.subSplitterRightWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.subProteinsTitleLabel = QLabel(self.subSplitterRightWidget)
        self.subProteinsTitleLabel.setObjectName(u"subProteinsTitleLabel")
        sizePolicy1.setHeightForWidth(self.subProteinsTitleLabel.sizePolicy().hasHeightForWidth())
        self.subProteinsTitleLabel.setSizePolicy(sizePolicy1)
        self.subProteinsTitleLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.subProteinsTitleLabel)

        self.subProteinsTableWidget = TableWidget(self.subSplitterRightWidget)
        if (self.subProteinsTableWidget.columnCount() < 3):
            self.subProteinsTableWidget.setColumnCount(3)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.subProteinsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.subProteinsTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.subProteinsTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem9)
        self.subProteinsTableWidget.setObjectName(u"subProteinsTableWidget")
        self.subProteinsTableWidget.setStyleSheet(u"QTableView:!active {selection-color: palette(Highlighted-Text);\n"
                                                  "                               selection-background-color: palette(Highlight);}\n"
                                                  "                           ")
        self.subProteinsTableWidget.setAutoScroll(False)
        self.subProteinsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.subProteinsTableWidget.setAlternatingRowColors(True)
        self.subProteinsTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.subProteinsTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.subProteinsTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.subProteinsTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.subProteinsTableWidget.setShowGrid(False)
        self.subProteinsTableWidget.setSortingEnabled(True)
        self.subProteinsTableWidget.setWordWrap(False)
        self.subProteinsTableWidget.setCornerButtonEnabled(False)
        self.subProteinsTableWidget.horizontalHeader().setStretchLastSection(False)
        self.subProteinsTableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_5.addWidget(self.subProteinsTableWidget)

        self.splitter.addWidget(self.subSplitterRightWidget)

        self.verticalLayout_3.addWidget(self.splitter)

        self.mainSplitter.addWidget(self.mainSplitterBottomWidget)

        self.verticalLayout_6.addWidget(self.mainSplitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1223, 29))
        self.fileMenu = QMenu(self.menuBar)
        self.fileMenu.setObjectName(u"fileMenu")
        self.fileMenu.setLocale(QLocale(QLocale.French, QLocale.France))
        self.databaseMenu = QMenu(self.menuBar)
        self.databaseMenu.setObjectName(u"databaseMenu")
        self.workingDigestionMenu = QMenu(self.menuBar)
        self.workingDigestionMenu.setObjectName(u"workingDigestionMenu")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menuBar.addAction(self.fileMenu.menuAction())
        self.menuBar.addAction(self.databaseMenu.menuAction())
        self.menuBar.addAction(self.workingDigestionMenu.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.fileMenu.addAction(self.createDatabaseAction)
        self.fileMenu.addAction(self.openDatabaseAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)
        self.databaseMenu.addAction(self.importFastaAction)
        self.databaseMenu.addAction(self.manageDigestionAction)
        self.menuHelp.addAction(self.aboutAction)

        self.retranslateUi(MainWindow)
        self.quitAction.triggered.connect(MainWindow.close)
        self.createDatabaseAction.triggered.connect(MainWindow.createDatabaseActionTriggered)
        self.openDatabaseAction.triggered.connect(MainWindow.openDatabaseActionTriggered)
        self.importFastaAction.triggered.connect(MainWindow.importFastaActionTriggered)
        self.proteinsSearchPushButton.clicked.connect(MainWindow.proteinsSearchPushButtonClicked)
        self.proteinsSearchLineEdit.returnPressed.connect(self.proteinsSearchPushButton.click)
        self.manageDigestionAction.triggered.connect(MainWindow.manageDigestionActionTriggered)
        self.proteinsTableWidget.itemSelectionChanged.connect(MainWindow.proteinsTableWidgetItemSelectionChanged)
        self.peptidesTableWidget.itemSelectionChanged.connect(MainWindow.peptidesTableWidgetItemSelectionChanged)
        self.aboutAction.triggered.connect(MainWindow.aboutActionTriggered)
        self.proteinsSearchLineEdit.textChanged.connect(MainWindow.proteinsSearchLineEditTextChanged)
        self.proteinsTableWidget.itemDoubleClicked.connect(MainWindow.refreshPeptidesTableWidget)
        self.peptidesTableWidget.itemDoubleClicked.connect(MainWindow.refreshSubProteinsTableWidget)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ProteinDigester", None))
        self.createDatabaseAction.setText(QCoreApplication.translate("MainWindow", u"Create digestion database", None))
        # if QT_CONFIG(shortcut)
        self.createDatabaseAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
        #endif // QT_CONFIG(shortcut)
        self.openDatabaseAction.setText(QCoreApplication.translate("MainWindow", u"Open digestion database", None))
        #if QT_CONFIG(shortcut)
        self.openDatabaseAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        #endif // QT_CONFIG(shortcut)
        self.importFastaAction.setText(QCoreApplication.translate("MainWindow", u"Import FASTA file", None))
        #if QT_CONFIG(shortcut)
        self.importFastaAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
        #endif // QT_CONFIG(shortcut)
        self.quitAction.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.manageDigestionAction.setText(QCoreApplication.translate("MainWindow", u"Manage digestion", None))
        #if QT_CONFIG(shortcut)
        self.manageDigestionAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+M", None))
        #endif // QT_CONFIG(shortcut)
        self.removeDigestionAction.setText(QCoreApplication.translate("MainWindow", u"Remove digestion", None))
        self.aboutAction.setText(QCoreApplication.translate("MainWindow", u"About ProteinDigester", None))
        self.proteinsTitleLabel.setText(QCoreApplication.translate("MainWindow",
                                                                   u"<html><head/><body><p><span style=\" font-weight:600;\">Proteins</span></p></body></html>",
                                                                   None))
        self.proteinsSearchLineEdit.setPlaceholderText("")
        self.proteinsSearchTypeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"By name", None))
        self.proteinsSearchTypeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"By sequence", None))
        self.proteinsSearchTypeComboBox.setItemText(2,
                                                    QCoreApplication.translate("MainWindow", u"By digest peptide", None))

        ___qtablewidgetitem = self.proteinsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"#", None));
        ___qtablewidgetitem1 = self.proteinsTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        self.peptideTitleLabel.setText(QCoreApplication.translate("MainWindow",
                                                                  u"<html><head/><body><p><span style=\" font-weight:600;\">Peptides from selected protein</span></p></body></html>",
                                                                  None))
        ___qtablewidgetitem2 = self.peptidesTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"#", None));
        ___qtablewidgetitem3 = self.peptidesTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Sequence", None));
        ___qtablewidgetitem4 = self.peptidesTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Missed cleavages", None));
        ___qtablewidgetitem5 = self.peptidesTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Digest unique", None));
        ___qtablewidgetitem6 = self.peptidesTableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Sequence unique", None));
        self.subProteinsTitleLabel.setText(QCoreApplication.translate("MainWindow",
                                                                      u"<html><head/><body><p><span style=\" font-weight:600;\">Proteins from selected peptide</span></p></body></html>",
                                                                      None))
        ___qtablewidgetitem7 = self.subProteinsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"#", None));
        ___qtablewidgetitem8 = self.subProteinsTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem9 = self.subProteinsTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Origin", None));
        self.fileMenu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.databaseMenu.setTitle(QCoreApplication.translate("MainWindow", u"Digestion database", None))
        self.workingDigestionMenu.setTitle(QCoreApplication.translate("MainWindow", u"Working digestion", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

