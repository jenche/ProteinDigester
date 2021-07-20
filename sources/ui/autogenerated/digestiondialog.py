# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'digestiondialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_DigestionDialog(object):
    def setupUi(self, DigestionDialog):
        if not DigestionDialog.objectName():
            DigestionDialog.setObjectName(u"DigestionDialog")
        DigestionDialog.resize(660, 265)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DigestionDialog.sizePolicy().hasHeightForWidth())
        DigestionDialog.setSizePolicy(sizePolicy)
        DigestionDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(DigestionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.enzymeComboBox = QComboBox(DigestionDialog)
        self.enzymeComboBox.setObjectName(u"enzymeComboBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.enzymeComboBox.sizePolicy().hasHeightForWidth())
        self.enzymeComboBox.setSizePolicy(sizePolicy1)
        self.enzymeComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.gridLayout.addWidget(self.enzymeComboBox, 0, 1, 1, 1)

        self.missedCleavagesLabel = QLabel(DigestionDialog)
        self.missedCleavagesLabel.setObjectName(u"missedCleavagesLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.missedCleavagesLabel.sizePolicy().hasHeightForWidth())
        self.missedCleavagesLabel.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.missedCleavagesLabel, 1, 0, 1, 1)

        self.missedCleavagesSpinBox = QSpinBox(DigestionDialog)
        self.missedCleavagesSpinBox.setObjectName(u"missedCleavagesSpinBox")
        sizePolicy1.setHeightForWidth(self.missedCleavagesSpinBox.sizePolicy().hasHeightForWidth())
        self.missedCleavagesSpinBox.setSizePolicy(sizePolicy1)
        self.missedCleavagesSpinBox.setFrame(True)
        self.missedCleavagesSpinBox.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout.addWidget(self.missedCleavagesSpinBox, 1, 1, 1, 1)

        self.enzymeLabel = QLabel(DigestionDialog)
        self.enzymeLabel.setObjectName(u"enzymeLabel")

        self.gridLayout.addWidget(self.enzymeLabel, 0, 0, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.enzymeDescriptionLabel = QLabel(DigestionDialog)
        self.enzymeDescriptionLabel.setObjectName(u"enzymeDescriptionLabel")
        self.enzymeDescriptionLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.enzymeDescriptionLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 6, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.addPushButton = QPushButton(DigestionDialog)
        self.addPushButton.setObjectName(u"addPushButton")

        self.horizontalLayout_2.addWidget(self.addPushButton)

        self.removePushButton = QPushButton(DigestionDialog)
        self.removePushButton.setObjectName(u"removePushButton")
        self.removePushButton.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.removePushButton)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.digestionSettingsTableWidget = QTableWidget(DigestionDialog)
        if (self.digestionSettingsTableWidget.columnCount() < 3):
            self.digestionSettingsTableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.digestionSettingsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.digestionSettingsTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.digestionSettingsTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.digestionSettingsTableWidget.setObjectName(u"digestionSettingsTableWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.digestionSettingsTableWidget.sizePolicy().hasHeightForWidth())
        self.digestionSettingsTableWidget.setSizePolicy(sizePolicy3)
        self.digestionSettingsTableWidget.setStyleSheet(
            u"QTableView:!active {selection-color: palette(Highlighted-Text);\n"
            "                  selection-background-color: palette(Highlight);}\n"
            "              ")
        self.digestionSettingsTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.digestionSettingsTableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.digestionSettingsTableWidget.setAutoScroll(False)
        self.digestionSettingsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.digestionSettingsTableWidget.setAlternatingRowColors(True)
        self.digestionSettingsTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.digestionSettingsTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.digestionSettingsTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.digestionSettingsTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.digestionSettingsTableWidget.setShowGrid(False)
        self.digestionSettingsTableWidget.setSortingEnabled(True)
        self.digestionSettingsTableWidget.setWordWrap(False)
        self.digestionSettingsTableWidget.setCornerButtonEnabled(False)
        self.digestionSettingsTableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.digestionSettingsTableWidget.verticalHeader().setVisible(False)

        self.horizontalLayout.addWidget(self.digestionSettingsTableWidget)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(DigestionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DigestionDialog)
        self.buttonBox.accepted.connect(DigestionDialog.accept)
        self.buttonBox.rejected.connect(DigestionDialog.reject)
        self.enzymeComboBox.currentTextChanged.connect(DigestionDialog.enzymeComboBoxCurrentTextChanged)
        self.addPushButton.clicked.connect(DigestionDialog.addPushButtonClicked)
        self.removePushButton.clicked.connect(DigestionDialog.removePushButtonClicked)
        self.digestionSettingsTableWidget.itemSelectionChanged.connect(
            DigestionDialog.digestionSettingsTableWidgetItemSelectionChanged)

        QMetaObject.connectSlotsByName(DigestionDialog)

    # setupUi

    def retranslateUi(self, DigestionDialog):
        DigestionDialog.setWindowTitle(QCoreApplication.translate("DigestionDialog", u"Manage digestion", None))
        self.missedCleavagesLabel.setText(
            QCoreApplication.translate("DigestionDialog", u"Maximum missed cleavages", None))
        self.enzymeLabel.setText(QCoreApplication.translate("DigestionDialog", u"Enzyme", None))
        self.enzymeDescriptionLabel.setText(QCoreApplication.translate("DigestionDialog",
                                                                       u"<html><head/><body><p><span style=\" font-style:italic;\">enzyme description</span></p></body></html>",
                                                                       None))
        self.addPushButton.setText(QCoreApplication.translate("DigestionDialog", u"Add", None))
        self.removePushButton.setText(QCoreApplication.translate("DigestionDialog", u"Remove", None))
        ___qtablewidgetitem = self.digestionSettingsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DigestionDialog", u"Enzyme", None));
        ___qtablewidgetitem1 = self.digestionSettingsTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DigestionDialog", u"Missed cleavages", None));
        ___qtablewidgetitem2 = self.digestionSettingsTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DigestionDialog", u"Rule", None));
    # retranslateUi
