# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import res_rc

class Ui_SettingsFrame(object):
    def setupUi(self, SettingsFrame):
        if not SettingsFrame.objectName():
            SettingsFrame.setObjectName(u"SettingsFrame")
        SettingsFrame.resize(619, 486)
        self.gridLayout_3 = QGridLayout(SettingsFrame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.equipment_group_box = QGroupBox(SettingsFrame)
        self.equipment_group_box.setObjectName(u"equipment_group_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.equipment_group_box.sizePolicy().hasHeightForWidth())
        self.equipment_group_box.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.equipment_group_box)
        self.gridLayout.setObjectName(u"gridLayout")
        self.guider_settings_button = QToolButton(self.equipment_group_box)
        self.guider_settings_button.setObjectName(u"guider_settings_button")
        self.guider_settings_button.setEnabled(False)
        icon = QIcon()
        icon.addFile(u":/icons/ic_settings_white_48px.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.guider_settings_button.setIcon(icon)
        self.guider_settings_button.setPopupMode(QToolButton.InstantPopup)

        self.gridLayout.addWidget(self.guider_settings_button, 1, 1, 1, 1)

        self.focuser_check_box = QCheckBox(self.equipment_group_box)
        self.focuser_check_box.setObjectName(u"focuser_check_box")

        self.gridLayout.addWidget(self.focuser_check_box, 4, 0, 1, 1)

        self.filter_wheel_check_box = QCheckBox(self.equipment_group_box)
        self.filter_wheel_check_box.setObjectName(u"filter_wheel_check_box")

        self.gridLayout.addWidget(self.filter_wheel_check_box, 3, 0, 1, 1)

        self.focuser_settings_button = QToolButton(self.equipment_group_box)
        self.focuser_settings_button.setObjectName(u"focuser_settings_button")
        self.focuser_settings_button.setEnabled(False)
        self.focuser_settings_button.setIcon(icon)
        self.focuser_settings_button.setPopupMode(QToolButton.InstantPopup)

        self.gridLayout.addWidget(self.focuser_settings_button, 4, 1, 1, 1)

        self.filter_wheel_settings_button = QToolButton(self.equipment_group_box)
        self.filter_wheel_settings_button.setObjectName(u"filter_wheel_settings_button")
        self.filter_wheel_settings_button.setEnabled(False)
        self.filter_wheel_settings_button.setIcon(icon)
        self.filter_wheel_settings_button.setPopupMode(QToolButton.InstantPopup)

        self.gridLayout.addWidget(self.filter_wheel_settings_button, 3, 1, 1, 1)

        self.camera_check_box = QCheckBox(self.equipment_group_box)
        self.camera_check_box.setObjectName(u"camera_check_box")

        self.gridLayout.addWidget(self.camera_check_box, 2, 0, 1, 1)

        self.guider_check_box = QCheckBox(self.equipment_group_box)
        self.guider_check_box.setObjectName(u"guider_check_box")

        self.gridLayout.addWidget(self.guider_check_box, 1, 0, 1, 1)

        self.telescope_settings_button = QToolButton(self.equipment_group_box)
        self.telescope_settings_button.setObjectName(u"telescope_settings_button")
        self.telescope_settings_button.setEnabled(False)
        self.telescope_settings_button.setIcon(icon)
        self.telescope_settings_button.setPopupMode(QToolButton.InstantPopup)

        self.gridLayout.addWidget(self.telescope_settings_button, 0, 1, 1, 1)

        self.telescope_check_box = QCheckBox(self.equipment_group_box)
        self.telescope_check_box.setObjectName(u"telescope_check_box")

        self.gridLayout.addWidget(self.telescope_check_box, 0, 0, 1, 1)

        self.camera_settings_button = QToolButton(self.equipment_group_box)
        self.camera_settings_button.setObjectName(u"camera_settings_button")
        self.camera_settings_button.setEnabled(False)
        self.camera_settings_button.setIcon(icon)
        self.camera_settings_button.setPopupMode(QToolButton.InstantPopup)

        self.gridLayout.addWidget(self.camera_settings_button, 2, 1, 1, 1)


        self.gridLayout_3.addWidget(self.equipment_group_box, 0, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.location_group_box = QGroupBox(SettingsFrame)
        self.location_group_box.setObjectName(u"location_group_box")
        sizePolicy.setHeightForWidth(self.location_group_box.sizePolicy().hasHeightForWidth())
        self.location_group_box.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.location_group_box)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lat_m_spin = QSpinBox(self.location_group_box)
        self.lat_m_spin.setObjectName(u"lat_m_spin")
        self.lat_m_spin.setFrame(True)
        self.lat_m_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.lat_m_spin.setKeyboardTracking(False)
        self.lat_m_spin.setProperty("showGroupSeparator", False)
        self.lat_m_spin.setMaximum(59)

        self.gridLayout_2.addWidget(self.lat_m_spin, 0, 2, 1, 1)

        self.lat_label = QLabel(self.location_group_box)
        self.lat_label.setObjectName(u"lat_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lat_label.sizePolicy().hasHeightForWidth())
        self.lat_label.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.lat_label, 0, 0, 1, 1)

        self.lat_s_spin = QSpinBox(self.location_group_box)
        self.lat_s_spin.setObjectName(u"lat_s_spin")
        self.lat_s_spin.setFrame(True)
        self.lat_s_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.lat_s_spin.setKeyboardTracking(False)
        self.lat_s_spin.setProperty("showGroupSeparator", False)
        self.lat_s_spin.setMaximum(59)

        self.gridLayout_2.addWidget(self.lat_s_spin, 0, 3, 1, 1)

        self.lat_d_spin = QSpinBox(self.location_group_box)
        self.lat_d_spin.setObjectName(u"lat_d_spin")
        self.lat_d_spin.setFrame(True)
        self.lat_d_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.lat_d_spin.setKeyboardTracking(False)
        self.lat_d_spin.setProperty("showGroupSeparator", False)
        self.lat_d_spin.setMinimum(-89)
        self.lat_d_spin.setMaximum(89)

        self.gridLayout_2.addWidget(self.lat_d_spin, 0, 1, 1, 1)

        self.long_m_spin = QSpinBox(self.location_group_box)
        self.long_m_spin.setObjectName(u"long_m_spin")
        self.long_m_spin.setFrame(True)
        self.long_m_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.long_m_spin.setKeyboardTracking(False)
        self.long_m_spin.setProperty("showGroupSeparator", False)
        self.long_m_spin.setMaximum(59)

        self.gridLayout_2.addWidget(self.long_m_spin, 1, 2, 1, 1)

        self.long_label = QLabel(self.location_group_box)
        self.long_label.setObjectName(u"long_label")
        sizePolicy1.setHeightForWidth(self.long_label.sizePolicy().hasHeightForWidth())
        self.long_label.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.long_label, 1, 0, 1, 1)

        self.long_d_spin = QSpinBox(self.location_group_box)
        self.long_d_spin.setObjectName(u"long_d_spin")
        self.long_d_spin.setFrame(True)
        self.long_d_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.long_d_spin.setKeyboardTracking(False)
        self.long_d_spin.setProperty("showGroupSeparator", False)
        self.long_d_spin.setMinimum(-179)
        self.long_d_spin.setMaximum(179)

        self.gridLayout_2.addWidget(self.long_d_spin, 1, 1, 1, 1)

        self.long_s_spin = QSpinBox(self.location_group_box)
        self.long_s_spin.setObjectName(u"long_s_spin")
        self.long_s_spin.setFrame(True)
        self.long_s_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.long_s_spin.setKeyboardTracking(False)
        self.long_s_spin.setProperty("showGroupSeparator", False)
        self.long_s_spin.setMaximum(59)

        self.gridLayout_2.addWidget(self.long_s_spin, 1, 3, 1, 1)


        self.gridLayout_3.addWidget(self.location_group_box, 1, 0, 1, 1)


        self.retranslateUi(SettingsFrame)
        self.telescope_check_box.toggled.connect(self.telescope_settings_button.setEnabled)
        self.guider_check_box.toggled.connect(self.guider_settings_button.setEnabled)
        self.camera_check_box.toggled.connect(self.camera_settings_button.setEnabled)
        self.filter_wheel_check_box.toggled.connect(self.filter_wheel_settings_button.setEnabled)
        self.focuser_check_box.toggled.connect(self.focuser_settings_button.setEnabled)

        QMetaObject.connectSlotsByName(SettingsFrame)
    # setupUi

    def retranslateUi(self, SettingsFrame):
        SettingsFrame.setWindowTitle(QCoreApplication.translate("SettingsFrame", u"Frame", None))
        self.equipment_group_box.setTitle(QCoreApplication.translate("SettingsFrame", u"Equipment", None))
        self.guider_settings_button.setText("")
        self.focuser_check_box.setText(QCoreApplication.translate("SettingsFrame", u"Focuser", None))
        self.filter_wheel_check_box.setText(QCoreApplication.translate("SettingsFrame", u"Filter wheel", None))
        self.focuser_settings_button.setText("")
        self.filter_wheel_settings_button.setText("")
        self.camera_check_box.setText(QCoreApplication.translate("SettingsFrame", u"Camera", None))
        self.guider_check_box.setText(QCoreApplication.translate("SettingsFrame", u"Guider", None))
        self.telescope_settings_button.setText("")
        self.telescope_check_box.setText(QCoreApplication.translate("SettingsFrame", u"Telescope", None))
        self.camera_settings_button.setText("")
        self.location_group_box.setTitle(QCoreApplication.translate("SettingsFrame", u"Location", None))
        self.lat_m_spin.setSuffix(QCoreApplication.translate("SettingsFrame", u"'", None))
        self.lat_label.setText(QCoreApplication.translate("SettingsFrame", u"Latitude", None))
        self.lat_s_spin.setSuffix(QCoreApplication.translate("SettingsFrame", u"\"", None))
        self.lat_d_spin.setSuffix(QCoreApplication.translate("SettingsFrame", u"\u00b0", None))
        self.long_m_spin.setSuffix(QCoreApplication.translate("SettingsFrame", u"'", None))
        self.long_label.setText(QCoreApplication.translate("SettingsFrame", u"Longitude", None))
        self.long_d_spin.setSuffix(QCoreApplication.translate("SettingsFrame", u"\u00b0", None))
        self.long_s_spin.setSuffix(QCoreApplication.translate("SettingsFrame", u"\"", None))
    # retranslateUi

