# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zwosettings.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ZWOSettings(object):
    def setupUi(self, ZWOSettings):
        ZWOSettings.setObjectName("ZWOSettings")
        ZWOSettings.resize(244, 172)
        ZWOSettings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        ZWOSettings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ZWOSettings)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinbox_gridlayout = QtWidgets.QGridLayout()
        self.spinbox_gridlayout.setObjectName("spinbox_gridlayout")
        self.temperature_label = QtWidgets.QLabel(ZWOSettings)
        self.temperature_label.setObjectName("temperature_label")
        self.spinbox_gridlayout.addWidget(self.temperature_label, 0, 0, 1, 1)
        self.temperature_spinbox = QtWidgets.QSpinBox(ZWOSettings)
        self.temperature_spinbox.setObjectName("temperature_spinbox")
        self.spinbox_gridlayout.addWidget(self.temperature_spinbox, 0, 1, 1, 1)
        self.brightness_label = QtWidgets.QLabel(ZWOSettings)
        self.brightness_label.setObjectName("brightness_label")
        self.spinbox_gridlayout.addWidget(self.brightness_label, 1, 0, 1, 1)
        self.brightness_spinbox = QtWidgets.QSpinBox(ZWOSettings)
        self.brightness_spinbox.setObjectName("brightness_spinbox")
        self.spinbox_gridlayout.addWidget(self.brightness_spinbox, 1, 1, 1, 1)
        self.gamma_label = QtWidgets.QLabel(ZWOSettings)
        self.gamma_label.setObjectName("gamma_label")
        self.spinbox_gridlayout.addWidget(self.gamma_label, 2, 0, 1, 1)
        self.gamma_spinbox = QtWidgets.QSpinBox(ZWOSettings)
        self.gamma_spinbox.setObjectName("gamma_spinbox")
        self.spinbox_gridlayout.addWidget(self.gamma_spinbox, 2, 1, 1, 1)
        self.red_label = QtWidgets.QLabel(ZWOSettings)
        self.red_label.setObjectName("red_label")
        self.spinbox_gridlayout.addWidget(self.red_label, 3, 0, 1, 1)
        self.red_spinbox = QtWidgets.QSpinBox(ZWOSettings)
        self.red_spinbox.setObjectName("red_spinbox")
        self.spinbox_gridlayout.addWidget(self.red_spinbox, 3, 1, 1, 1)
        self.blue_label = QtWidgets.QLabel(ZWOSettings)
        self.blue_label.setObjectName("blue_label")
        self.spinbox_gridlayout.addWidget(self.blue_label, 4, 0, 1, 1)
        self.blue_spinbox = QtWidgets.QSpinBox(ZWOSettings)
        self.blue_spinbox.setObjectName("blue_spinbox")
        self.spinbox_gridlayout.addWidget(self.blue_spinbox, 4, 1, 1, 1)
        self.usb_label = QtWidgets.QLabel(ZWOSettings)
        self.usb_label.setObjectName("usb_label")
        self.spinbox_gridlayout.addWidget(self.usb_label, 5, 0, 1, 1)
        self.usb_spinbox = QtWidgets.QSpinBox(ZWOSettings)
        self.usb_spinbox.setObjectName("usb_spinbox")
        self.spinbox_gridlayout.addWidget(self.usb_spinbox, 5, 1, 1, 1)
        self.horizontalLayout.addLayout(self.spinbox_gridlayout)
        self.line = QtWidgets.QFrame(ZWOSettings)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.checkbox_gridlayout = QtWidgets.QGridLayout()
        self.checkbox_gridlayout.setObjectName("checkbox_gridlayout")
        self.highspeed_checkbox = QtWidgets.QCheckBox(ZWOSettings)
        self.highspeed_checkbox.setObjectName("highspeed_checkbox")
        self.checkbox_gridlayout.addWidget(self.highspeed_checkbox, 0, 0, 1, 1)
        self.verticalflip_checkbox = QtWidgets.QCheckBox(ZWOSettings)
        self.verticalflip_checkbox.setObjectName("verticalflip_checkbox")
        self.checkbox_gridlayout.addWidget(self.verticalflip_checkbox, 4, 0, 1, 1)
        self.monobin_checkbox = QtWidgets.QCheckBox(ZWOSettings)
        self.monobin_checkbox.setObjectName("monobin_checkbox")
        self.checkbox_gridlayout.addWidget(self.monobin_checkbox, 2, 0, 1, 1)
        self.hardwarebin_checkbox = QtWidgets.QCheckBox(ZWOSettings)
        self.hardwarebin_checkbox.setObjectName("hardwarebin_checkbox")
        self.checkbox_gridlayout.addWidget(self.hardwarebin_checkbox, 1, 0, 1, 1)
        self.horizontalflip_checkbox = QtWidgets.QCheckBox(ZWOSettings)
        self.horizontalflip_checkbox.setObjectName("horizontalflip_checkbox")
        self.checkbox_gridlayout.addWidget(self.horizontalflip_checkbox, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.checkbox_gridlayout.addItem(spacerItem, 5, 0, 1, 1)
        self.horizontalLayout.addLayout(self.checkbox_gridlayout)

        self.retranslateUi(ZWOSettings)
        QtCore.QMetaObject.connectSlotsByName(ZWOSettings)

    def retranslateUi(self, ZWOSettings):
        _translate = QtCore.QCoreApplication.translate
        ZWOSettings.setWindowTitle(_translate("ZWOSettings", "Frame"))
        self.temperature_label.setText(_translate("ZWOSettings", "Temperature"))
        self.brightness_label.setText(_translate("ZWOSettings", "Brightness"))
        self.gamma_label.setText(_translate("ZWOSettings", "Gamma"))
        self.red_label.setText(_translate("ZWOSettings", "Red"))
        self.blue_label.setText(_translate("ZWOSettings", "Blue"))
        self.usb_label.setText(_translate("ZWOSettings", "USB Bandwidth"))
        self.highspeed_checkbox.setText(_translate("ZWOSettings", "High Speed"))
        self.verticalflip_checkbox.setText(_translate("ZWOSettings", "Vertical Flip"))
        self.monobin_checkbox.setText(_translate("ZWOSettings", "Mono Bin"))
        self.hardwarebin_checkbox.setText(_translate("ZWOSettings", "Hardware Bin"))
        self.horizontalflip_checkbox.setText(_translate("ZWOSettings", "Horizontal Flip"))

