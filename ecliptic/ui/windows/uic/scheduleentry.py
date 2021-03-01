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
        self.add_button.setText("")
        self.remove_button.setText("")
        self.reset_button.setText("")
    # retranslateUi

