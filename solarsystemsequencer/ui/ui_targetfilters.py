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
        TargetFilters.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(TargetFilters)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filter_tablewidget = QtWidgets.QTableWidget(TargetFilters)
        self.filter_tablewidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.filter_tablewidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.filter_tablewidget.setObjectName("filter_tablewidget")
        self.filter_tablewidget.setColumnCount(4)
        self.filter_tablewidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.filter_tablewidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filter_tablewidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.filter_tablewidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.filter_tablewidget.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.filter_tablewidget)
        self.buttonbox_layout = QtWidgets.QHBoxLayout()
        self.buttonbox_layout.setContentsMargins(9, -1, 9, 9)
        self.buttonbox_layout.setObjectName("buttonbox_layout")
        self.buttonbox = QtWidgets.QDialogButtonBox(TargetFilters)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName("buttonbox")
        self.buttonbox_layout.addWidget(self.buttonbox)
        self.verticalLayout.addLayout(self.buttonbox_layout)

        self.retranslateUi(TargetFilters)
        self.buttonbox.accepted.connect(TargetFilters.accept)
        self.buttonbox.rejected.connect(TargetFilters.reject)
        QtCore.QMetaObject.connectSlotsByName(TargetFilters)

    def retranslateUi(self, TargetFilters):
        _translate = QtCore.QCoreApplication.translate
        item = self.filter_tablewidget.horizontalHeaderItem(0)
        item.setText(_translate("TargetFilters", "Use"))
        item = self.filter_tablewidget.horizontalHeaderItem(1)
        item.setText(_translate("TargetFilters", "Exposure"))
        item = self.filter_tablewidget.horizontalHeaderItem(2)
        item.setText(_translate("TargetFilters", "Gain"))
        item = self.filter_tablewidget.horizontalHeaderItem(3)
        item.setText(_translate("TargetFilters", "Integration"))

