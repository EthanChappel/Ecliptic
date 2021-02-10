# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'guider.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import res_rc

class Ui_GuiderFrame(object):
    def setupUi(self, GuiderFrame):
        if not GuiderFrame.objectName():
            GuiderFrame.setObjectName(u"GuiderFrame")
        GuiderFrame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(GuiderFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.guider_scrollarea = QScrollArea(GuiderFrame)
        self.guider_scrollarea.setObjectName(u"guider_scrollarea")
        self.guider_scrollarea.setLayoutDirection(Qt.LeftToRight)
        self.guider_scrollarea.setFrameShape(QFrame.NoFrame)
        self.guider_scrollarea.setFrameShadow(QFrame.Plain)
        self.guider_scrollarea.setLineWidth(0)
        self.guider_scrollarea.setWidgetResizable(True)
        self.guider_scrollarea.setAlignment(Qt.AlignCenter)
        self.guiderscrollareawidgetcontents = QWidget()
        self.guiderscrollareawidgetcontents.setObjectName(u"guiderscrollareawidgetcontents")
        self.guiderscrollareawidgetcontents.setGeometry(QRect(0, 0, 400, 231))
        self.verticalLayout_6 = QVBoxLayout(self.guiderscrollareawidgetcontents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.guider_preview_label = QLabel(self.guiderscrollareawidgetcontents)
        self.guider_preview_label.setObjectName(u"guider_preview_label")
        self.guider_preview_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.guider_preview_label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.guider_scrollarea.setWidget(self.guiderscrollareawidgetcontents)

        self.verticalLayout.addWidget(self.guider_scrollarea)

        self.guider_gridlayout = QGridLayout()
        self.guider_gridlayout.setObjectName(u"guider_gridlayout")
        self.guider_gridlayout.setContentsMargins(11, -1, 11, -1)
        self.guiderzoom_label = QLabel(GuiderFrame)
        self.guiderzoom_label.setObjectName(u"guiderzoom_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.guiderzoom_label.sizePolicy().hasHeightForWidth())
        self.guiderzoom_label.setSizePolicy(sizePolicy)

        self.guider_gridlayout.addWidget(self.guiderzoom_label, 0, 0, 1, 1)

        self.guiderzoom_spinbox = QSpinBox(GuiderFrame)
        self.guiderzoom_spinbox.setObjectName(u"guiderzoom_spinbox")
        self.guiderzoom_spinbox.setMinimum(20)
        self.guiderzoom_spinbox.setMaximum(300)
        self.guiderzoom_spinbox.setValue(100)

        self.guider_gridlayout.addWidget(self.guiderzoom_spinbox, 0, 1, 1, 1)

        self.guiderzoom_slider = QSlider(GuiderFrame)
        self.guiderzoom_slider.setObjectName(u"guiderzoom_slider")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.guiderzoom_slider.sizePolicy().hasHeightForWidth())
        self.guiderzoom_slider.setSizePolicy(sizePolicy1)
        self.guiderzoom_slider.setMinimum(20)
        self.guiderzoom_slider.setMaximum(300)
        self.guiderzoom_slider.setValue(100)
        self.guiderzoom_slider.setOrientation(Qt.Horizontal)

        self.guider_gridlayout.addWidget(self.guiderzoom_slider, 1, 0, 1, 2)

        self.guiderzoom_line = QFrame(GuiderFrame)
        self.guiderzoom_line.setObjectName(u"guiderzoom_line")
        self.guiderzoom_line.setFrameShape(QFrame.VLine)
        self.guiderzoom_line.setFrameShadow(QFrame.Sunken)

        self.guider_gridlayout.addWidget(self.guiderzoom_line, 0, 2, 2, 1)

        self.guiderzoom_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.guider_gridlayout.addItem(self.guiderzoom_spacer, 0, 4, 2, 1)

        self.solve_center_button = QPushButton(GuiderFrame)
        self.solve_center_button.setObjectName(u"solve_center_button")
        self.solve_center_button.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.solve_center_button.sizePolicy().hasHeightForWidth())
        self.solve_center_button.setSizePolicy(sizePolicy2)
        self.solve_center_button.setIconSize(QSize(24, 24))
        self.solve_center_button.setAutoDefault(True)

        self.guider_gridlayout.addWidget(self.solve_center_button, 1, 3, 1, 1)

        self.plate_solve_button = QPushButton(GuiderFrame)
        self.plate_solve_button.setObjectName(u"plate_solve_button")
        self.plate_solve_button.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.plate_solve_button.sizePolicy().hasHeightForWidth())
        self.plate_solve_button.setSizePolicy(sizePolicy2)
        self.plate_solve_button.setIconSize(QSize(24, 24))
        self.plate_solve_button.setAutoDefault(True)

        self.guider_gridlayout.addWidget(self.plate_solve_button, 0, 3, 1, 1)


        self.verticalLayout.addLayout(self.guider_gridlayout)


        self.retranslateUi(GuiderFrame)

        self.solve_center_button.setDefault(False)
        self.plate_solve_button.setDefault(False)


        QMetaObject.connectSlotsByName(GuiderFrame)
    # setupUi

    def retranslateUi(self, GuiderFrame):
        GuiderFrame.setWindowTitle(QCoreApplication.translate("GuiderFrame", u"Frame", None))
        self.guider_preview_label.setText("")
        self.guiderzoom_label.setText(QCoreApplication.translate("GuiderFrame", u"Zoom", None))
        self.guiderzoom_spinbox.setSuffix(QCoreApplication.translate("GuiderFrame", u"%", None))
        self.solve_center_button.setText(QCoreApplication.translate("GuiderFrame", u"Solve && Center", None))
        self.plate_solve_button.setText(QCoreApplication.translate("GuiderFrame", u"Plate Solve", None))
    # retranslateUi

