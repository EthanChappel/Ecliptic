# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'zwosettings.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_ZWOSettings(object):
    def setupUi(self, ZWOSettings):
        if not ZWOSettings.objectName():
            ZWOSettings.setObjectName(u"ZWOSettings")
        ZWOSettings.resize(429, 196)
        ZWOSettings.setFrameShape(QFrame.StyledPanel)
        ZWOSettings.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(ZWOSettings)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinbox_gridlayout = QGridLayout()
        self.spinbox_gridlayout.setObjectName(u"spinbox_gridlayout")
        self.red_label = QLabel(ZWOSettings)
        self.red_label.setObjectName(u"red_label")

        self.spinbox_gridlayout.addWidget(self.red_label, 2, 0, 1, 1)

        self.gamma_label = QLabel(ZWOSettings)
        self.gamma_label.setObjectName(u"gamma_label")

        self.spinbox_gridlayout.addWidget(self.gamma_label, 1, 0, 1, 1)

        self.gamma_spinbox = QSpinBox(ZWOSettings)
        self.gamma_spinbox.setObjectName(u"gamma_spinbox")

        self.spinbox_gridlayout.addWidget(self.gamma_spinbox, 1, 1, 1, 1)

        self.blue_spinbox = QSpinBox(ZWOSettings)
        self.blue_spinbox.setObjectName(u"blue_spinbox")

        self.spinbox_gridlayout.addWidget(self.blue_spinbox, 3, 1, 1, 1)

        self.red_spinbox = QSpinBox(ZWOSettings)
        self.red_spinbox.setObjectName(u"red_spinbox")

        self.spinbox_gridlayout.addWidget(self.red_spinbox, 2, 1, 1, 1)

        self.blue_label = QLabel(ZWOSettings)
        self.blue_label.setObjectName(u"blue_label")

        self.spinbox_gridlayout.addWidget(self.blue_label, 3, 0, 1, 1)

        self.temperature_label = QLabel(ZWOSettings)
        self.temperature_label.setObjectName(u"temperature_label")

        self.spinbox_gridlayout.addWidget(self.temperature_label, 0, 0, 1, 1)

        self.temperature_spinbox = QSpinBox(ZWOSettings)
        self.temperature_spinbox.setObjectName(u"temperature_spinbox")

        self.spinbox_gridlayout.addWidget(self.temperature_spinbox, 0, 1, 1, 1)

        self.usb_spinbox = QSpinBox(ZWOSettings)
        self.usb_spinbox.setObjectName(u"usb_spinbox")

        self.spinbox_gridlayout.addWidget(self.usb_spinbox, 4, 1, 1, 1)

        self.usb_label = QLabel(ZWOSettings)
        self.usb_label.setObjectName(u"usb_label")

        self.spinbox_gridlayout.addWidget(self.usb_label, 4, 0, 1, 1)


        self.horizontalLayout.addLayout(self.spinbox_gridlayout)

        self.line = QFrame(ZWOSettings)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.checkbox_gridlayout = QGridLayout()
        self.checkbox_gridlayout.setObjectName(u"checkbox_gridlayout")
        self.horizontalflip_checkbox = QCheckBox(ZWOSettings)
        self.horizontalflip_checkbox.setObjectName(u"horizontalflip_checkbox")

        self.checkbox_gridlayout.addWidget(self.horizontalflip_checkbox, 2, 0, 1, 1)

        self.hardwarebin_checkbox = QCheckBox(ZWOSettings)
        self.hardwarebin_checkbox.setObjectName(u"hardwarebin_checkbox")

        self.checkbox_gridlayout.addWidget(self.hardwarebin_checkbox, 1, 0, 1, 1)

        self.highspeed_checkbox = QCheckBox(ZWOSettings)
        self.highspeed_checkbox.setObjectName(u"highspeed_checkbox")

        self.checkbox_gridlayout.addWidget(self.highspeed_checkbox, 0, 0, 1, 1)

        self.checkbox_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.checkbox_gridlayout.addItem(self.checkbox_spacer, 4, 0, 1, 1)

        self.verticalflip_checkbox = QCheckBox(ZWOSettings)
        self.verticalflip_checkbox.setObjectName(u"verticalflip_checkbox")

        self.checkbox_gridlayout.addWidget(self.verticalflip_checkbox, 3, 0, 1, 1)


        self.horizontalLayout.addLayout(self.checkbox_gridlayout)


        self.retranslateUi(ZWOSettings)

        QMetaObject.connectSlotsByName(ZWOSettings)
    # setupUi

    def retranslateUi(self, ZWOSettings):
        ZWOSettings.setWindowTitle(QCoreApplication.translate("ZWOSettings", u"Frame", None))
        self.red_label.setText(QCoreApplication.translate("ZWOSettings", u"Red", None))
        self.gamma_label.setText(QCoreApplication.translate("ZWOSettings", u"Gamma", None))
        self.blue_label.setText(QCoreApplication.translate("ZWOSettings", u"Blue", None))
        self.temperature_label.setText(QCoreApplication.translate("ZWOSettings", u"Temperature", None))
        self.usb_label.setText(QCoreApplication.translate("ZWOSettings", u"USB Bandwidth", None))
        self.horizontalflip_checkbox.setText(QCoreApplication.translate("ZWOSettings", u"Horizontal Flip", None))
        self.hardwarebin_checkbox.setText(QCoreApplication.translate("ZWOSettings", u"Bin", None))
        self.highspeed_checkbox.setText(QCoreApplication.translate("ZWOSettings", u"High Speed", None))
        self.verticalflip_checkbox.setText(QCoreApplication.translate("ZWOSettings", u"Vertical Flip", None))
    # retranslateUi

