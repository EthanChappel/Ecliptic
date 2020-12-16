# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filters.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import res_rc

class Ui_FiltersFrame(object):
    def setupUi(self, FiltersFrame):
        if not FiltersFrame.objectName():
            FiltersFrame.setObjectName(u"FiltersFrame")
        FiltersFrame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(FiltersFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.table = QTableWidget(FiltersFrame)
        if (self.table.columnCount() < 5):
            self.table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.table.setObjectName(u"table")
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setLineWidth(0)
        self.table.setSortingEnabled(False)

        self.verticalLayout.addWidget(self.table)

        self.horizontallayout_14 = QHBoxLayout()
        self.horizontallayout_14.setObjectName(u"horizontallayout_14")
        self.horizontallayout_14.setContentsMargins(9, -1, 9, -1)
        self.add_button = QPushButton(FiltersFrame)
        self.add_button.setObjectName(u"add_button")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/icons/ic_add_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.add_button.setIcon(icon)
        self.add_button.setAutoDefault(True)

        self.horizontallayout_14.addWidget(self.add_button)

        self.remove_button = QPushButton(FiltersFrame)
        self.remove_button.setObjectName(u"remove_button")
        sizePolicy.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u":/icons/ic_remove_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_button.setIcon(icon1)
        self.remove_button.setAutoDefault(True)

        self.horizontallayout_14.addWidget(self.remove_button)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontallayout_14.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontallayout_14)


        self.retranslateUi(FiltersFrame)

        QMetaObject.connectSlotsByName(FiltersFrame)
    # setupUi

    def retranslateUi(self, FiltersFrame):
        FiltersFrame.setWindowTitle(QCoreApplication.translate("FiltersFrame", u"Frame", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FiltersFrame", u"Name", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem.setToolTip(QCoreApplication.translate("FiltersFrame", u"The name of the filter", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FiltersFrame", u"Brand", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FiltersFrame", u"Wheel Position", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem2.setToolTip(QCoreApplication.translate("FiltersFrame", u"The position the filter lies in the filter wheel", None));
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem3 = self.table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FiltersFrame", u"Lower Cutoff", None));
        ___qtablewidgetitem4 = self.table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("FiltersFrame", u"Upper Cutoff", None));
#if QT_CONFIG(tooltip)
        self.add_button.setToolTip(QCoreApplication.translate("FiltersFrame", u"Add row", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.remove_button.setToolTip(QCoreApplication.translate("FiltersFrame", u"Remove row", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

