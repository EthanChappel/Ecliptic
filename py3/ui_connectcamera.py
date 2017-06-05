# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connectcamera.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConnectCamera(object):
    def setupUi(self, ConnectCamera):
        ConnectCamera.setObjectName("ConnectCamera")
        ConnectCamera.resize(254, 209)
        ConnectCamera.setStyleSheet("QRadioButton{font: bold;}")
        self.gridLayout = QtWidgets.QGridLayout(ConnectCamera)
        self.gridLayout.setObjectName("gridLayout")
        self.asi_radio = QtWidgets.QRadioButton(ConnectCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asi_radio.sizePolicy().hasHeightForWidth())
        self.asi_radio.setSizePolicy(sizePolicy)
        self.asi_radio.setObjectName("asi_radio")
        self.gridLayout.addWidget(self.asi_radio, 3, 0, 1, 1)
        self.asi_combobox = QtWidgets.QComboBox(ConnectCamera)
        self.asi_combobox.setObjectName("asi_combobox")
        self.gridLayout.addWidget(self.asi_combobox, 3, 1, 1, 1)
        self.asi_sync_button = QtWidgets.QPushButton(ConnectCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asi_sync_button.sizePolicy().hasHeightForWidth())
        self.asi_sync_button.setSizePolicy(sizePolicy)
        self.asi_sync_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/ic_sync_white_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.asi_sync_button.setIcon(icon)
        self.asi_sync_button.setObjectName("asi_sync_button")
        self.gridLayout.addWidget(self.asi_sync_button, 3, 2, 1, 1)
        self.ascom_label = QtWidgets.QLabel(ConnectCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ascom_label.sizePolicy().hasHeightForWidth())
        self.ascom_label.setSizePolicy(sizePolicy)
        self.ascom_label.setWordWrap(True)
        self.ascom_label.setObjectName("ascom_label")
        self.gridLayout.addWidget(self.ascom_label, 2, 0, 1, 3)
        self.ascom_radio = QtWidgets.QRadioButton(ConnectCamera)
        self.ascom_radio.setObjectName("ascom_radio")
        self.gridLayout.addWidget(self.ascom_radio, 1, 0, 1, 3)
        self.instruct_label = QtWidgets.QLabel(ConnectCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instruct_label.sizePolicy().hasHeightForWidth())
        self.instruct_label.setSizePolicy(sizePolicy)
        self.instruct_label.setWordWrap(True)
        self.instruct_label.setObjectName("instruct_label")
        self.gridLayout.addWidget(self.instruct_label, 0, 0, 1, 3)
        self.buttonbox = QtWidgets.QDialogButtonBox(ConnectCamera)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonbox.setObjectName("buttonbox")
        self.gridLayout.addWidget(self.buttonbox, 6, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 3)
        self.asi_label = QtWidgets.QLabel(ConnectCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asi_label.sizePolicy().hasHeightForWidth())
        self.asi_label.setSizePolicy(sizePolicy)
        self.asi_label.setWordWrap(True)
        self.asi_label.setObjectName("asi_label")
        self.gridLayout.addWidget(self.asi_label, 4, 0, 1, 3)

        self.retranslateUi(ConnectCamera)
        self.buttonbox.accepted.connect(ConnectCamera.accept)
        self.buttonbox.rejected.connect(ConnectCamera.reject)
        QtCore.QMetaObject.connectSlotsByName(ConnectCamera)

    def retranslateUi(self, ConnectCamera):
        _translate = QtCore.QCoreApplication.translate
        ConnectCamera.setWindowTitle(_translate("ConnectCamera", "Solar System Sequencer - Connect Camera"))
        self.asi_radio.setText(_translate("ConnectCamera", "ZWO ASI"))
        self.ascom_label.setText(_translate("ConnectCamera", "Connect an ASCOM camera. Data acquisition is slow compared to ASI Cameras"))
        self.ascom_radio.setText(_translate("ConnectCamera", "ASCOM"))
        self.instruct_label.setText(_translate("ConnectCamera", "Select the camera you would like to connect."))
        self.asi_label.setText(_translate("ConnectCamera", "Connect a ZWO ASI camera."))

import res_rc
