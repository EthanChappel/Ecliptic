# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'guiderparameters.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_GuiderParameters(object):
    def setupUi(self, GuiderParameters):
        if not GuiderParameters.objectName():
            GuiderParameters.setObjectName(u"GuiderParameters")
        GuiderParameters.resize(198, 171)
        GuiderParameters.setFrameShape(QFrame.StyledPanel)
        GuiderParameters.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(GuiderParameters)
        self.gridLayout.setObjectName(u"gridLayout")
        self.northoffset_dial = QDial(GuiderParameters)
        self.northoffset_dial.setObjectName(u"northoffset_dial")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.northoffset_dial.sizePolicy().hasHeightForWidth())
        self.northoffset_dial.setSizePolicy(sizePolicy)
        self.northoffset_dial.setMinimum(-180)
        self.northoffset_dial.setMaximum(180)
        self.northoffset_dial.setWrapping(True)
        self.northoffset_dial.setNotchesVisible(True)

        self.gridLayout.addWidget(self.northoffset_dial, 2, 1, 2, 1)

        self.parameters_layout = QHBoxLayout()
        self.parameters_layout.setObjectName(u"parameters_layout")
        self.parameters_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.formlayout = QFormLayout()
        self.formlayout.setObjectName(u"formlayout")
        self.formlayout.setSizeConstraint(QLayout.SetFixedSize)
        self.ra_label = QLabel(GuiderParameters)
        self.ra_label.setObjectName(u"ra_label")

        self.formlayout.setWidget(0, QFormLayout.LabelRole, self.ra_label)

        self.ra_spinbox = QSpinBox(GuiderParameters)
        self.ra_spinbox.setObjectName(u"ra_spinbox")
        self.ra_spinbox.setMinimum(-100)
        self.ra_spinbox.setMaximum(100)
        self.ra_spinbox.setValue(10)

        self.formlayout.setWidget(0, QFormLayout.FieldRole, self.ra_spinbox)

        self.dec_label = QLabel(GuiderParameters)
        self.dec_label.setObjectName(u"dec_label")

        self.formlayout.setWidget(1, QFormLayout.LabelRole, self.dec_label)

        self.dec_spinBox = QSpinBox(GuiderParameters)
        self.dec_spinBox.setObjectName(u"dec_spinBox")
        self.dec_spinBox.setMinimum(-100)
        self.dec_spinBox.setMaximum(100)
        self.dec_spinBox.setValue(10)

        self.formlayout.setWidget(1, QFormLayout.FieldRole, self.dec_spinBox)


        self.parameters_layout.addLayout(self.formlayout)

        self.every_label = QLabel(GuiderParameters)
        self.every_label.setObjectName(u"every_label")

        self.parameters_layout.addWidget(self.every_label)

        self.seconds_spinbox = QDoubleSpinBox(GuiderParameters)
        self.seconds_spinbox.setObjectName(u"seconds_spinbox")
        self.seconds_spinbox.setDecimals(1)
        self.seconds_spinbox.setMinimum(0.100000000000000)
        self.seconds_spinbox.setValue(2.000000000000000)

        self.parameters_layout.addWidget(self.seconds_spinbox)


        self.gridLayout.addLayout(self.parameters_layout, 0, 0, 1, 2)

        self.northoffset_spinbox = QSpinBox(GuiderParameters)
        self.northoffset_spinbox.setObjectName(u"northoffset_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.northoffset_spinbox.sizePolicy().hasHeightForWidth())
        self.northoffset_spinbox.setSizePolicy(sizePolicy1)
        self.northoffset_spinbox.setMinimum(-180)
        self.northoffset_spinbox.setMaximum(180)

        self.gridLayout.addWidget(self.northoffset_spinbox, 3, 0, 1, 1, Qt.AlignTop)

        self.northoffset_label = QLabel(GuiderParameters)
        self.northoffset_label.setObjectName(u"northoffset_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.northoffset_label.sizePolicy().hasHeightForWidth())
        self.northoffset_label.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.northoffset_label, 2, 0, 1, 1, Qt.AlignBottom)

        self.line = QFrame(GuiderParameters)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)


        self.retranslateUi(GuiderParameters)
        self.northoffset_spinbox.valueChanged.connect(self.northoffset_dial.setValue)
        self.northoffset_dial.valueChanged.connect(self.northoffset_spinbox.setValue)

        QMetaObject.connectSlotsByName(GuiderParameters)
    # setupUi

    def retranslateUi(self, GuiderParameters):
        GuiderParameters.setWindowTitle(QCoreApplication.translate("GuiderParameters", u"Frame", None))
        self.ra_label.setText(QCoreApplication.translate("GuiderParameters", u"Right Ascension", None))
        self.ra_spinbox.setSuffix(QCoreApplication.translate("GuiderParameters", u"\"", None))
        self.dec_label.setText(QCoreApplication.translate("GuiderParameters", u"Declination", None))
        self.dec_spinBox.setSuffix(QCoreApplication.translate("GuiderParameters", u"\"", None))
        self.every_label.setText(QCoreApplication.translate("GuiderParameters", u"every", None))
        self.seconds_spinbox.setSuffix(QCoreApplication.translate("GuiderParameters", u"s", None))
        self.northoffset_label.setText(QCoreApplication.translate("GuiderParameters", u"North Offset", None))
    # retranslateUi

