# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filter_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_FilterSettingsFrame(object):
    def setupUi(self, FilterSettingsFrame):
        if not FilterSettingsFrame.objectName():
            FilterSettingsFrame.setObjectName(u"FilterSettingsFrame")
        FilterSettingsFrame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(FilterSettingsFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.filter_table = QTableWidget(FilterSettingsFrame)
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


        self.retranslateUi(FilterSettingsFrame)

        QMetaObject.connectSlotsByName(FilterSettingsFrame)
    # setupUi

    def retranslateUi(self, FilterSettingsFrame):
        FilterSettingsFrame.setWindowTitle(QCoreApplication.translate("FilterSettingsFrame", u"Frame", None))
        ___qtablewidgetitem = self.filter_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FilterSettingsFrame", u"Filter", None));
        ___qtablewidgetitem1 = self.filter_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FilterSettingsFrame", u"Exposure", None));
        ___qtablewidgetitem2 = self.filter_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FilterSettingsFrame", u"Gain", None));
        ___qtablewidgetitem3 = self.filter_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FilterSettingsFrame", u"Bin", None));
        ___qtablewidgetitem4 = self.filter_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FilterSettingsFrame", u"Limit", None));
        ___qtablewidgetitem5 = self.filter_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("FilterSettingsFrame", u"Format", None));
    # retranslateUi

