# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_CameraFrame(object):
    def setupUi(self, CameraFrame):
        if not CameraFrame.objectName():
            CameraFrame.setObjectName(u"CameraFrame")
        CameraFrame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(CameraFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.camera_scrollarea = QScrollArea(CameraFrame)
        self.camera_scrollarea.setObjectName(u"camera_scrollarea")
        self.camera_scrollarea.setLayoutDirection(Qt.LeftToRight)
        self.camera_scrollarea.setFrameShape(QFrame.NoFrame)
        self.camera_scrollarea.setFrameShadow(QFrame.Plain)
        self.camera_scrollarea.setLineWidth(0)
        self.camera_scrollarea.setWidgetResizable(True)
        self.camera_scrollarea.setAlignment(Qt.AlignCenter)
        self.camera_scrollarea_contents = QWidget()
        self.camera_scrollarea_contents.setObjectName(u"camera_scrollarea_contents")
        self.camera_scrollarea_contents.setGeometry(QRect(0, 0, 400, 229))
        self.verticalLayout_4 = QVBoxLayout(self.camera_scrollarea_contents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.camera_preview_label = QLabel(self.camera_scrollarea_contents)
        self.camera_preview_label.setObjectName(u"camera_preview_label")
        self.camera_preview_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.camera_preview_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.camera_scrollarea.setWidget(self.camera_scrollarea_contents)

        self.verticalLayout.addWidget(self.camera_scrollarea)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(11, -1, 11, -1)
        self.camera_zoom_label = QLabel(CameraFrame)
        self.camera_zoom_label.setObjectName(u"camera_zoom_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_zoom_label.sizePolicy().hasHeightForWidth())
        self.camera_zoom_label.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.camera_zoom_label, 0, 0, 1, 1)

        self.camera_zoom_spinbox = QSpinBox(CameraFrame)
        self.camera_zoom_spinbox.setObjectName(u"camera_zoom_spinbox")
        self.camera_zoom_spinbox.setMinimum(20)
        self.camera_zoom_spinbox.setMaximum(300)
        self.camera_zoom_spinbox.setValue(100)

        self.gridLayout_6.addWidget(self.camera_zoom_spinbox, 0, 1, 1, 1)

        self.camera_zoom_slider = QSlider(CameraFrame)
        self.camera_zoom_slider.setObjectName(u"camera_zoom_slider")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.camera_zoom_slider.sizePolicy().hasHeightForWidth())
        self.camera_zoom_slider.setSizePolicy(sizePolicy1)
        self.camera_zoom_slider.setMinimum(20)
        self.camera_zoom_slider.setMaximum(300)
        self.camera_zoom_slider.setValue(100)
        self.camera_zoom_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_6.addWidget(self.camera_zoom_slider, 1, 0, 1, 2)

        self.camera_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.camera_spacer, 0, 2, 2, 1)


        self.verticalLayout.addLayout(self.gridLayout_6)


        self.retranslateUi(CameraFrame)

        QMetaObject.connectSlotsByName(CameraFrame)
    # setupUi

    def retranslateUi(self, CameraFrame):
        CameraFrame.setWindowTitle(QCoreApplication.translate("CameraFrame", u"Frame", None))
        self.camera_preview_label.setText("")
        self.camera_zoom_label.setText(QCoreApplication.translate("CameraFrame", u"Zoom", None))
        self.camera_zoom_spinbox.setSuffix(QCoreApplication.translate("CameraFrame", u"%", None))
    # retranslateUi

