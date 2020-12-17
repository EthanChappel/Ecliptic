# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connectcamera.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import res_rc

class Ui_ConnectCamera(object):
    def setupUi(self, ConnectCamera):
        if not ConnectCamera.objectName():
            ConnectCamera.setObjectName(u"ConnectCamera")
        ConnectCamera.resize(287, 259)
        ConnectCamera.setStyleSheet(u"QRadioButton{font: bold;}")
        self.verticalLayout_2 = QVBoxLayout(ConnectCamera)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stackedWidget = QStackedWidget(ConnectCamera)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.camera_page = QWidget()
        self.camera_page.setObjectName(u"camera_page")
        self.verticalLayout = QVBoxLayout(self.camera_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.instruct_label = QLabel(self.camera_page)
        self.instruct_label.setObjectName(u"instruct_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instruct_label.sizePolicy().hasHeightForWidth())
        self.instruct_label.setSizePolicy(sizePolicy)
        self.instruct_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.instruct_label, 0, Qt.AlignTop)

        self.ascom_commandlink = QCommandLinkButton(self.camera_page)
        self.ascom_commandlink.setObjectName(u"ascom_commandlink")
        icon = QIcon()
        icon.addFile(u":/thirdparty/ascom_logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ascom_commandlink.setIcon(icon)

        self.verticalLayout.addWidget(self.ascom_commandlink)

        self.asi_commandlink = QCommandLinkButton(self.camera_page)
        self.asi_commandlink.setObjectName(u"asi_commandlink")
        self.asi_commandlink.setEnabled(False)
        icon1 = QIcon()
        icon1.addFile(u":/thirdparty/asi_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.asi_commandlink.setIcon(icon1)

        self.verticalLayout.addWidget(self.asi_commandlink)

        self.stackedWidget.addWidget(self.camera_page)
        self.ascom_commandlink.raise_()
        self.asi_commandlink.raise_()
        self.instruct_label.raise_()
        self.asi_page = QWidget()
        self.asi_page.setObjectName(u"asi_page")
        self.gridLayout = QGridLayout(self.asi_page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 2)

        self.label = QLabel(self.asi_page)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.asi_combobox = QComboBox(self.asi_page)
        self.asi_combobox.setObjectName(u"asi_combobox")

        self.gridLayout.addWidget(self.asi_combobox, 2, 1, 1, 1)

        self.asi_label = QLabel(self.asi_page)
        self.asi_label.setObjectName(u"asi_label")
        sizePolicy.setHeightForWidth(self.asi_label.sizePolicy().hasHeightForWidth())
        self.asi_label.setSizePolicy(sizePolicy)
        self.asi_label.setWordWrap(True)

        self.gridLayout.addWidget(self.asi_label, 0, 0, 1, 2, Qt.AlignTop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)

        self.asi_connect_button = QPushButton(self.asi_page)
        self.asi_connect_button.setObjectName(u"asi_connect_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.asi_connect_button.sizePolicy().hasHeightForWidth())
        self.asi_connect_button.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.asi_connect_button, 2, 2, 1, 1)

        self.stackedWidget.addWidget(self.asi_page)

        self.verticalLayout_2.addWidget(self.stackedWidget)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.vertical_spacer)

        self.buttonbox = QDialogButtonBox(ConnectCamera)
        self.buttonbox.setObjectName(u"buttonbox")
        self.buttonbox.setOrientation(Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Cancel)

        self.verticalLayout_2.addWidget(self.buttonbox)


        self.retranslateUi(ConnectCamera)
        self.buttonbox.accepted.connect(ConnectCamera.accept)
        self.buttonbox.rejected.connect(ConnectCamera.reject)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ConnectCamera)
    # setupUi

    def retranslateUi(self, ConnectCamera):
        ConnectCamera.setWindowTitle(QCoreApplication.translate("ConnectCamera", u"Ecliptic - Connect Camera", None))
        self.instruct_label.setText(QCoreApplication.translate("ConnectCamera", u"Select the camera you would like to connect.", None))
        self.ascom_commandlink.setText(QCoreApplication.translate("ConnectCamera", u"ASCOM Camera", None))
        self.ascom_commandlink.setDescription(QCoreApplication.translate("ConnectCamera", u"Connect an ASCOM camera. Data acquisition is currently slow compared to ZWO ASI Cameras", None))
        self.asi_commandlink.setText(QCoreApplication.translate("ConnectCamera", u"ZWO ASI Camera", None))
        self.asi_commandlink.setDescription(QCoreApplication.translate("ConnectCamera", u"Connect a ZWO ASI camera.", None))
        self.label.setText(QCoreApplication.translate("ConnectCamera", u"ZWO ASI Camera", None))
        self.asi_label.setText(QCoreApplication.translate("ConnectCamera", u"Connect a ZWO ASI camera.", None))
        self.asi_connect_button.setText(QCoreApplication.translate("ConnectCamera", u"Connect", None))
    # retranslateUi

