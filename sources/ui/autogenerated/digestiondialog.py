# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'digestiondialog.ui',
# licensing of 'digestiondialog.ui' applies.
#
# Created: Mon Feb 10 21:00:49 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets

class Ui_DigestionDialog(object):
    def setupUi(self, DigestionDialog):
        DigestionDialog.setObjectName("DigestionDialog")
        DigestionDialog.resize(660, 265)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DigestionDialog.sizePolicy().hasHeightForWidth())
        DigestionDialog.setSizePolicy(sizePolicy)
        DigestionDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DigestionDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.enzymeComboBox = QtWidgets.QComboBox(DigestionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enzymeComboBox.sizePolicy().hasHeightForWidth())
        self.enzymeComboBox.setSizePolicy(sizePolicy)
        self.enzymeComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.enzymeComboBox.setObjectName("enzymeComboBox")
        self.gridLayout.addWidget(self.enzymeComboBox, 0, 1, 1, 1)
        self.missedCleavagesLabel = QtWidgets.QLabel(DigestionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.missedCleavagesLabel.sizePolicy().hasHeightForWidth())
        self.missedCleavagesLabel.setSizePolicy(sizePolicy)
        self.missedCleavagesLabel.setObjectName("missedCleavagesLabel")
        self.gridLayout.addWidget(self.missedCleavagesLabel, 1, 0, 1, 1)
        self.missedCleavagesSpinBox = QtWidgets.QSpinBox(DigestionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.missedCleavagesSpinBox.sizePolicy().hasHeightForWidth())
        self.missedCleavagesSpinBox.setSizePolicy(sizePolicy)
        self.missedCleavagesSpinBox.setFrame(True)
        self.missedCleavagesSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.missedCleavagesSpinBox.setObjectName("missedCleavagesSpinBox")
        self.gridLayout.addWidget(self.missedCleavagesSpinBox, 1, 1, 1, 1)
        self.enzymeLabel = QtWidgets.QLabel(DigestionDialog)
        self.enzymeLabel.setObjectName("enzymeLabel")
        self.gridLayout.addWidget(self.enzymeLabel, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.enzymeDescriptionLabel = QtWidgets.QLabel(DigestionDialog)
        self.enzymeDescriptionLabel.setWordWrap(True)
        self.enzymeDescriptionLabel.setObjectName("enzymeDescriptionLabel")
        self.verticalLayout_2.addWidget(self.enzymeDescriptionLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.addPushButton = QtWidgets.QPushButton(DigestionDialog)
        self.addPushButton.setObjectName("addPushButton")
        self.horizontalLayout_2.addWidget(self.addPushButton)
        self.removePushButton = QtWidgets.QPushButton(DigestionDialog)
        self.removePushButton.setEnabled(False)
        self.removePushButton.setObjectName("removePushButton")
        self.horizontalLayout_2.addWidget(self.removePushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.digestionSettingsTableWidget = QtWidgets.QTableWidget(DigestionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.digestionSettingsTableWidget.sizePolicy().hasHeightForWidth())
        self.digestionSettingsTableWidget.setSizePolicy(sizePolicy)
        self.digestionSettingsTableWidget.setStyleSheet(
            "QTableView:!active  {selection-color: palette(Highlighted-Text); selection-background-color: palette(Highlight);}")
        self.digestionSettingsTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.digestionSettingsTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.digestionSettingsTableWidget.setAutoScroll(False)
        self.digestionSettingsTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.digestionSettingsTableWidget.setAlternatingRowColors(True)
        self.digestionSettingsTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.digestionSettingsTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.digestionSettingsTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.digestionSettingsTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.digestionSettingsTableWidget.setShowGrid(False)
        self.digestionSettingsTableWidget.setWordWrap(False)
        self.digestionSettingsTableWidget.setCornerButtonEnabled(False)
        self.digestionSettingsTableWidget.setObjectName("digestionSettingsTableWidget")
        self.digestionSettingsTableWidget.setColumnCount(3)
        self.digestionSettingsTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.digestionSettingsTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.digestionSettingsTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.digestionSettingsTableWidget.setHorizontalHeaderItem(2, item)
        self.digestionSettingsTableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.digestionSettingsTableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.digestionSettingsTableWidget)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(DigestionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DigestionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DigestionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DigestionDialog.reject)
        QtCore.QObject.connect(self.enzymeComboBox, QtCore.SIGNAL("currentTextChanged(QString)"), DigestionDialog.enzymeComboBoxCurrentTextChanged)
        QtCore.QObject.connect(self.addPushButton, QtCore.SIGNAL("clicked()"), DigestionDialog.addPushButtonClicked)
        QtCore.QObject.connect(self.removePushButton, QtCore.SIGNAL("clicked()"), DigestionDialog.removePushButtonClicked)
        QtCore.QObject.connect(self.digestionSettingsTableWidget, QtCore.SIGNAL("itemSelectionChanged()"), DigestionDialog.digestionSettingsTableWidgetItemSelectionChanged)
        QtCore.QMetaObject.connectSlotsByName(DigestionDialog)

    def retranslateUi(self, DigestionDialog):
        DigestionDialog.setWindowTitle(QtWidgets.QApplication.translate("DigestionDialog", "Manage digestion", None, -1))
        self.missedCleavagesLabel.setText(QtWidgets.QApplication.translate("DigestionDialog", "Maximum missed cleavages", None, -1))
        self.enzymeLabel.setText(QtWidgets.QApplication.translate("DigestionDialog", "Enzyme", None, -1))
        self.enzymeDescriptionLabel.setText(QtWidgets.QApplication.translate("DigestionDialog", "<html><head/><body><p><span style=\" font-style:italic;\">enzyme description</span></p></body></html>", None, -1))
        self.addPushButton.setText(QtWidgets.QApplication.translate("DigestionDialog", "Add", None, -1))
        self.removePushButton.setText(QtWidgets.QApplication.translate("DigestionDialog", "Remove", None, -1))
        self.digestionSettingsTableWidget.setSortingEnabled(True)
        self.digestionSettingsTableWidget.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("DigestionDialog", "Enzyme", None, -1))
        self.digestionSettingsTableWidget.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("DigestionDialog", "Missed cleavages", None, -1))
        self.digestionSettingsTableWidget.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("DigestionDialog", "Rule", None, -1))

