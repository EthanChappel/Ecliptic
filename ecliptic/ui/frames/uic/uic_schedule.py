# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'schedule.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import res_rc

class Ui_ScheduleFrame(object):
    def setupUi(self, ScheduleFrame):
        if not ScheduleFrame.objectName():
            ScheduleFrame.setObjectName(u"ScheduleFrame")
        ScheduleFrame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ScheduleFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.schedule_table = QTableWidget(ScheduleFrame)
        if (self.schedule_table.columnCount() < 4):
            self.schedule_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setText(u"ID");
        self.schedule_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.schedule_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.schedule_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.schedule_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.schedule_table.setObjectName(u"schedule_table")
        self.schedule_table.setFrameShape(QFrame.NoFrame)
        self.schedule_table.setSortingEnabled(True)
        self.schedule_table.horizontalHeader().setCascadingSectionResizes(True)
        self.schedule_table.horizontalHeader().setDefaultSectionSize(150)
        self.schedule_table.horizontalHeader().setStretchLastSection(True)
        self.schedule_table.verticalHeader().setCascadingSectionResizes(True)

        self.verticalLayout.addWidget(self.schedule_table)

        self.horizontallayout = QHBoxLayout()
        self.horizontallayout.setObjectName(u"horizontallayout")
        self.horizontallayout.setContentsMargins(9, -1, 9, -1)
        self.addrow_button = QPushButton(ScheduleFrame)
        self.addrow_button.setObjectName(u"addrow_button")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addrow_button.sizePolicy().hasHeightForWidth())
        self.addrow_button.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/icons/ic_add_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addrow_button.setIcon(icon)
        self.addrow_button.setAutoDefault(True)

        self.horizontallayout.addWidget(self.addrow_button)

        self.removerow_button = QPushButton(ScheduleFrame)
        self.removerow_button.setObjectName(u"removerow_button")
        sizePolicy.setHeightForWidth(self.removerow_button.sizePolicy().hasHeightForWidth())
        self.removerow_button.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u":/icons/ic_remove_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.removerow_button.setIcon(icon1)
        self.removerow_button.setAutoDefault(True)

        self.horizontallayout.addWidget(self.removerow_button)

        self.horizontalspacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontallayout.addItem(self.horizontalspacer_3)


        self.verticalLayout.addLayout(self.horizontallayout)


        self.retranslateUi(ScheduleFrame)

        QMetaObject.connectSlotsByName(ScheduleFrame)
    # setupUi

    def retranslateUi(self, ScheduleFrame):
        ScheduleFrame.setWindowTitle(QCoreApplication.translate("ScheduleFrame", u"Frame", None))
        ___qtablewidgetitem = self.schedule_table.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ScheduleFrame", u"Date & Time", None));
        ___qtablewidgetitem1 = self.schedule_table.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ScheduleFrame", u"Target", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem1.setToolTip(QCoreApplication.translate("ScheduleFrame", u"The target to aim at.", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem2 = self.schedule_table.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ScheduleFrame", u"Parameters", None));
#if QT_CONFIG(tooltip)
        self.addrow_button.setToolTip(QCoreApplication.translate("ScheduleFrame", u"Add row", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.removerow_button.setToolTip(QCoreApplication.translate("ScheduleFrame", u"Remove row", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

