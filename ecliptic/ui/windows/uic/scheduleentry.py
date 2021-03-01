# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scheduleentry.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import res_rc

class Ui_ScheduleEntryDialog(object):
    def setupUi(self, ScheduleEntryDialog):
        if not ScheduleEntryDialog.objectName():
            ScheduleEntryDialog.setObjectName(u"ScheduleEntryDialog")
        ScheduleEntryDialog.resize(514, 329)
        ScheduleEntryDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(ScheduleEntryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.filter_table = QTableWidget(ScheduleEntryDialog)
        if (self.filter_table.columnCount() < 6):
            self.filter_table.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.filter_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.filter_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.filter_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.filter_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.filter_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.filter_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.filter_table.setObjectName(u"filter_table")
        self.filter_table.setFrameShape(QFrame.NoFrame)
        self.filter_table.setFrameShadow(QFrame.Plain)

        self.verticalLayout.addWidget(self.filter_table)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, -1, 9, 9)
        self.add_button = QPushButton(ScheduleEntryDialog)
        self.add_button.setObjectName(u"add_button")
        icon = QIcon()
        icon.addFile(u":/icons/ic_add_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.add_button.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.add_button)

        self.remove_button = QPushButton(ScheduleEntryDialog)
        self.remove_button.setObjectName(u"remove_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ic_remove_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.remove_button)

        self.reset_button = QPushButton(ScheduleEntryDialog)
        self.reset_button.setObjectName(u"reset_button")
        icon2 = QIcon()
        icon2.addFile(u":/icons/ic_replay_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.reset_button.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.reset_button)

        self.button_box = QDialogButtonBox(ScheduleEntryDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_2.addWidget(self.button_box)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ScheduleEntryDialog)
        self.button_box.accepted.connect(ScheduleEntryDialog.accept)
        self.button_box.rejected.connect(ScheduleEntryDialog.reject)

        QMetaObject.connectSlotsByName(ScheduleEntryDialog)
    # setupUi

    def retranslateUi(self, ScheduleEntryDialog):
        ScheduleEntryDialog.setWindowTitle("")
        ___qtablewidgetitem = self.filter_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Filter", None));
        ___qtablewidgetitem1 = self.filter_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Exposure", None));
        ___qtablewidgetitem2 = self.filter_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Gain", None));
        ___qtablewidgetitem3 = self.filter_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Bin", None));
        ___qtablewidgetitem4 = self.filter_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Limit", None));
        ___qtablewidgetitem5 = self.filter_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Format", None));
        self.add_button.setText("")
        self.remove_button.setText("")
        self.reset_button.setText("")
    # retranslateUi

