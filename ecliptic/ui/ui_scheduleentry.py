# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scheduleentry.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import res_rc

class Ui_ScheduleEntryDialog(object):
    def setupUi(self, ScheduleEntryDialog):
        if not ScheduleEntryDialog.objectName():
            ScheduleEntryDialog.setObjectName(u"ScheduleEntryDialog")
        ScheduleEntryDialog.resize(650, 450)
        ScheduleEntryDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(ScheduleEntryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.filters_group_box = QGroupBox(ScheduleEntryDialog)
        self.filters_group_box.setObjectName(u"filters_group_box")
        self.verticalLayout_2 = QVBoxLayout(self.filters_group_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, -1)
        self.filter_table = QTableWidget(self.filters_group_box)
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

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(11, -1, 11, -1)
        self.add_filter_button = QPushButton(self.filters_group_box)
        self.add_filter_button.setObjectName(u"add_filter_button")
        icon = QIcon()
        icon.addFile(u":/icons/ic_add_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.add_filter_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.add_filter_button)

        self.remove_filter_button = QPushButton(self.filters_group_box)
        self.remove_filter_button.setObjectName(u"remove_filter_button")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ic_remove_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_filter_button.setIcon(icon1)

        self.horizontalLayout.addWidget(self.remove_filter_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.filters_group_box)

        self.solve_group_box = QGroupBox(ScheduleEntryDialog)
        self.solve_group_box.setObjectName(u"solve_group_box")
        self.horizontalLayout_2 = QHBoxLayout(self.solve_group_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.solve_group_box)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.down_sample_combo_box = QComboBox(self.solve_group_box)
        self.down_sample_combo_box.addItem("")
        self.down_sample_combo_box.addItem("")
        self.down_sample_combo_box.addItem("")
        self.down_sample_combo_box.addItem("")
        self.down_sample_combo_box.addItem("")
        self.down_sample_combo_box.addItem("")
        self.down_sample_combo_box.setObjectName(u"down_sample_combo_box")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.down_sample_combo_box)


        self.horizontalLayout_2.addLayout(self.formLayout)

        self.line = QFrame(self.solve_group_box)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(self.solve_group_box)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.search_radius_spin_box = QSpinBox(self.solve_group_box)
        self.search_radius_spin_box.setObjectName(u"search_radius_spin_box")
        self.search_radius_spin_box.setMinimum(1)
        self.search_radius_spin_box.setMaximum(180)
        self.search_radius_spin_box.setValue(20)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.search_radius_spin_box)


        self.horizontalLayout_2.addLayout(self.formLayout_2)

        self.line_2 = QFrame(self.solve_group_box)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_2)

        self.debug_check_box = QCheckBox(self.solve_group_box)
        self.debug_check_box.setObjectName(u"debug_check_box")

        self.horizontalLayout_2.addWidget(self.debug_check_box)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.solve_group_box)

        self.button_box = QDialogButtonBox(ScheduleEntryDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(ScheduleEntryDialog)
        self.button_box.accepted.connect(ScheduleEntryDialog.accept)
        self.button_box.rejected.connect(ScheduleEntryDialog.reject)

        QMetaObject.connectSlotsByName(ScheduleEntryDialog)
    # setupUi

    def retranslateUi(self, ScheduleEntryDialog):
        ScheduleEntryDialog.setWindowTitle("")
        self.filters_group_box.setTitle(QCoreApplication.translate("ScheduleEntryDialog", u"Filters", None))
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
        self.solve_group_box.setTitle(QCoreApplication.translate("ScheduleEntryDialog", u"Plate Solving", None))
        self.label.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Down sample", None))
        self.down_sample_combo_box.setItemText(0, QCoreApplication.translate("ScheduleEntryDialog", u"Default", None))
        self.down_sample_combo_box.setItemText(1, QCoreApplication.translate("ScheduleEntryDialog", u"Auto", None))
        self.down_sample_combo_box.setItemText(2, QCoreApplication.translate("ScheduleEntryDialog", u"1", None))
        self.down_sample_combo_box.setItemText(3, QCoreApplication.translate("ScheduleEntryDialog", u"2", None))
        self.down_sample_combo_box.setItemText(4, QCoreApplication.translate("ScheduleEntryDialog", u"3", None))
        self.down_sample_combo_box.setItemText(5, QCoreApplication.translate("ScheduleEntryDialog", u"4", None))

        self.label_2.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Search radius", None))
        self.search_radius_spin_box.setSuffix(QCoreApplication.translate("ScheduleEntryDialog", u"\u00b0", None))
        self.debug_check_box.setText(QCoreApplication.translate("ScheduleEntryDialog", u"Open ASTAP window before solve", None))
    # retranslateUi

