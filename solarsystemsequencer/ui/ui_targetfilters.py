# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'targetfilters.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TargetFilters(object):
    def setupUi(self, TargetFilters):
        TargetFilters.setObjectName("TargetFilters")
        TargetFilters.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(TargetFilters)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.filters_table = QtWidgets.QTableWidget(TargetFilters)
        self.filters_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.filters_table.setFrameShadow(QtWidgets.QFrame.Plain)
        self.filters_table.setObjectName("filters_table")
        self.filters_table.setColumnCount(4)
        self.filters_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.filters_table.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.filters_table, 0, 0, 1, 1)
        self.buttonbox_layout = QtWidgets.QHBoxLayout()
        self.buttonbox_layout.setContentsMargins(9, -1, 9, 9)
        self.buttonbox_layout.setObjectName("buttonbox_layout")
        self.targets_label = QtWidgets.QLabel(TargetFilters)
        self.targets_label.setObjectName("targets_label")
        self.buttonbox_layout.addWidget(self.targets_label)
        self.targets_combobox = QtWidgets.QComboBox(TargetFilters)
        self.targets_combobox.setObjectName("targets_combobox")
        self.buttonbox_layout.addWidget(self.targets_combobox)
        self.buttonbox = QtWidgets.QDialogButtonBox(TargetFilters)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName("buttonbox")
        self.buttonbox_layout.addWidget(self.buttonbox)
        self.gridLayout.addLayout(self.buttonbox_layout, 1, 0, 1, 1)

        self.retranslateUi(TargetFilters)
        self.buttonbox.accepted.connect(TargetFilters.accept)
        self.buttonbox.rejected.connect(TargetFilters.reject)
        QtCore.QMetaObject.connectSlotsByName(TargetFilters)

    def retranslateUi(self, TargetFilters):
        _translate = QtCore.QCoreApplication.translate
        TargetFilters.setWindowTitle(_translate("TargetFilters", "Solar System Sequencer - Filter Presets"))
        item = self.filters_table.horizontalHeaderItem(0)
        item.setText(_translate("TargetFilters", "Use"))
        item = self.filters_table.horizontalHeaderItem(1)
        item.setText(_translate("TargetFilters", "Exposure"))
        item = self.filters_table.horizontalHeaderItem(2)
        item.setText(_translate("TargetFilters", "Gain"))
        item = self.filters_table.horizontalHeaderItem(3)
        item.setText(_translate("TargetFilters", "Integration"))
        self.targets_label.setText(_translate("TargetFilters", "Target"))

