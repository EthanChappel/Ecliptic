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
        ScheduleEntryDialog.resize(650, 550)
        self.verticalLayout = QVBoxLayout(ScheduleEntryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tab_widget = QTabWidget(ScheduleEntryDialog)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        self.tab_widget.setDocumentMode(True)
        self.capture_tab = QWidget()
        self.capture_tab.setObjectName(u"capture_tab")
        self.verticalLayout_2 = QVBoxLayout(self.capture_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.filter_table = QTableWidget(self.capture_tab)
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

        self.verticalLayout_2.addWidget(self.filter_table)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(11, -1, 11, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.add_filter_button = QPushButton(self.capture_tab)
        self.add_filter_button.setObjectName(u"add_filter_button")
        icon = QIcon()
        icon.addFile(u":/icons/ic_add_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.add_filter_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.add_filter_button)

        self.remove_filter_button = QPushButton(self.capture_tab)
        self.remove_filter_button.setObjectName(u"remove_filter_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ic_remove_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_filter_button.setIcon(icon1)

        self.horizontalLayout.addWidget(self.remove_filter_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.tab_widget.addTab(self.capture_tab, "")
        self.astrometry_tab = QWidget()
        self.astrometry_tab.setObjectName(u"astrometry_tab")
        self.tab_widget.addTab(self.astrometry_tab, "")

        self.verticalLayout.addWidget(self.tab_widget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(11, -1, 11, 11)
        self.line = QFrame(ScheduleEntryDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.button_box = QDialogButtonBox(ScheduleEntryDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)

        self.verticalLayout_3.addWidget(self.button_box)


        self.verticalLayout.addLayout(self.verticalLayout_3)


        self.retranslateUi(ScheduleEntryDialog)
        self.button_box.accepted.connect(ScheduleEntryDialog.accept)
        self.button_box.rejected.connect(ScheduleEntryDialog.reject)

        self.tab_widget.setCurrentIndex(0)


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
        self.add_filter_button.setText("")
        self.remove_filter_button.setText("")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.capture_tab), QCoreApplication.translate("ScheduleEntryDialog", u"Capture", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.astrometry_tab), QCoreApplication.translate("ScheduleEntryDialog", u"Astrometry", None))
    # retranslateUi

