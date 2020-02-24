# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'targetfilters.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_TargetFilters(object):
    def setupUi(self, TargetFilters):
        if TargetFilters.objectName():
            TargetFilters.setObjectName(u"TargetFilters")
        TargetFilters.resize(400, 300)
        self.gridLayout = QGridLayout(TargetFilters)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.filters_table = QTableWidget(TargetFilters)
        if (self.filters_table.columnCount() < 4):
            self.filters_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.filters_table.setObjectName(u"filters_table")
        self.filters_table.setFrameShape(QFrame.NoFrame)
        self.filters_table.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self.filters_table, 0, 0, 1, 1)

        self.buttonbox_layout = QHBoxLayout()
        self.buttonbox_layout.setObjectName(u"buttonbox_layout")
        self.buttonbox_layout.setContentsMargins(9, -1, 9, 9)
        self.targets_label = QLabel(TargetFilters)
        self.targets_label.setObjectName(u"targets_label")

        self.buttonbox_layout.addWidget(self.targets_label)

        self.targets_combobox = QComboBox(TargetFilters)
        self.targets_combobox.setObjectName(u"targets_combobox")

        self.buttonbox_layout.addWidget(self.targets_combobox)

        self.buttonbox = QDialogButtonBox(TargetFilters)
        self.buttonbox.setObjectName(u"buttonbox")
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.buttonbox_layout.addWidget(self.buttonbox)


        self.gridLayout.addLayout(self.buttonbox_layout, 1, 0, 1, 1)


        self.retranslateUi(TargetFilters)
        self.buttonbox.accepted.connect(TargetFilters.accept)
        self.buttonbox.rejected.connect(TargetFilters.reject)

        QMetaObject.connectSlotsByName(TargetFilters)
    # setupUi

    def retranslateUi(self, TargetFilters):
        TargetFilters.setWindowTitle(QCoreApplication.translate("TargetFilters", u"Solar System Sequencer - Filter Presets", None))
        ___qtablewidgetitem = self.filters_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("TargetFilters", u"Use", None));
        ___qtablewidgetitem1 = self.filters_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("TargetFilters", u"Exposure", None));
        ___qtablewidgetitem2 = self.filters_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("TargetFilters", u"Gain", None));
        ___qtablewidgetitem3 = self.filters_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("TargetFilters", u"Integration", None));
        self.targets_label.setText(QCoreApplication.translate("TargetFilters", u"Target", None))
    # retranslateUi

