# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import res_rc

class Ui_SettingsFrame(object):
    def setupUi(self, SettingsFrame):
        if not SettingsFrame.objectName():
            SettingsFrame.setObjectName(u"SettingsFrame")
        SettingsFrame.resize(622, 487)
        self.verticalLayout_2 = QVBoxLayout(SettingsFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(SettingsFrame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -254, 605, 741))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.equipment_group_box = QGroupBox(self.scrollAreaWidgetContents)
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


        self.verticalLayout.addWidget(self.equipment_group_box)

        self.location_group_box = QGroupBox(self.scrollAreaWidgetContents)
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


        self.verticalLayout.addWidget(self.location_group_box)

        self.observer_group_box = QGroupBox(self.scrollAreaWidgetContents)
        self.observer_group_box.setObjectName(u"observer_group_box")
        self.formLayout = QFormLayout(self.observer_group_box)
        self.formLayout.setObjectName(u"formLayout")
        self.observer_name_label = QLabel(self.observer_group_box)
        self.observer_name_label.setObjectName(u"observer_name_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.observer_name_label)

        self.observer_telescope_label = QLabel(self.observer_group_box)
        self.observer_telescope_label.setObjectName(u"observer_telescope_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.observer_telescope_label)

        self.observer_camera_label = QLabel(self.observer_group_box)
        self.observer_camera_label.setObjectName(u"observer_camera_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.observer_camera_label)

        self.observer_name_combo_box = QComboBox(self.observer_group_box)
        self.observer_name_combo_box.setObjectName(u"observer_name_combo_box")
        self.observer_name_combo_box.setEditable(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.observer_name_combo_box)

        self.observer_telescope_combo_box = QComboBox(self.observer_group_box)
        self.observer_telescope_combo_box.setObjectName(u"observer_telescope_combo_box")
        self.observer_telescope_combo_box.setEditable(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.observer_telescope_combo_box)

        self.observer_camera_combo_box = QComboBox(self.observer_group_box)
        self.observer_camera_combo_box.setObjectName(u"observer_camera_combo_box")
        self.observer_camera_combo_box.setEditable(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.observer_camera_combo_box)


        self.verticalLayout.addWidget(self.observer_group_box)

        self.filters_group_box = QGroupBox(self.scrollAreaWidgetContents)
        self.filters_group_box.setObjectName(u"filters_group_box")

        self.verticalLayout.addWidget(self.filters_group_box)

        self.plate_solving_group_box = QGroupBox(self.scrollAreaWidgetContents)
        self.plate_solving_group_box.setObjectName(u"plate_solving_group_box")
        self.formLayout_2 = QFormLayout(self.plate_solving_group_box)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.astap_radio = QRadioButton(self.plate_solving_group_box)
        self.astap_radio.setObjectName(u"astap_radio")
        self.astap_radio.setEnabled(False)
        self.astap_radio.setChecked(True)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.astap_radio)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.astap_location_line_edit = QLineEdit(self.plate_solving_group_box)
        self.astap_location_line_edit.setObjectName(u"astap_location_line_edit")

        self.horizontalLayout.addWidget(self.astap_location_line_edit)

        self.astap_location_button = QPushButton(self.plate_solving_group_box)
        self.astap_location_button.setObjectName(u"astap_location_button")
        self.astap_location_button.setAutoDefault(True)

        self.horizontalLayout.addWidget(self.astap_location_button)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.label = QLabel(self.plate_solving_group_box)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.label)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.search_radius_label = QLabel(self.plate_solving_group_box)
        self.search_radius_label.setObjectName(u"search_radius_label")

        self.horizontalLayout_4.addWidget(self.search_radius_label)

        self.search_radius_spin_box = QSpinBox(self.plate_solving_group_box)
        self.search_radius_spin_box.setObjectName(u"search_radius_spin_box")
        self.search_radius_spin_box.setMinimum(1)
        self.search_radius_spin_box.setMaximum(180)
        self.search_radius_spin_box.setSingleStep(2)
        self.search_radius_spin_box.setValue(20)

        self.horizontalLayout_4.addWidget(self.search_radius_spin_box)

        self.line_2 = QFrame(self.plate_solving_group_box)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_4.addWidget(self.line_2)

        self.downsample_label = QLabel(self.plate_solving_group_box)
        self.downsample_label.setObjectName(u"downsample_label")

        self.horizontalLayout_4.addWidget(self.downsample_label)

        self.downsample_combo_box = QComboBox(self.plate_solving_group_box)
        self.downsample_combo_box.addItem("")
        self.downsample_combo_box.addItem("")
        self.downsample_combo_box.addItem("")
        self.downsample_combo_box.addItem("")
        self.downsample_combo_box.addItem("")
        self.downsample_combo_box.setObjectName(u"downsample_combo_box")

        self.horizontalLayout_4.addWidget(self.downsample_combo_box)

        self.line_3 = QFrame(self.plate_solving_group_box)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_4.addWidget(self.line_3)

        self.plate_solve_debug_check_box = QCheckBox(self.plate_solving_group_box)
        self.plate_solve_debug_check_box.setObjectName(u"plate_solve_debug_check_box")

        self.horizontalLayout_4.addWidget(self.plate_solve_debug_check_box)


        self.formLayout_2.setLayout(4, QFormLayout.SpanningRole, self.horizontalLayout_4)

        self.line = QFrame(self.plate_solving_group_box)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.formLayout_2.setWidget(3, QFormLayout.SpanningRole, self.line)


        self.verticalLayout.addWidget(self.plate_solving_group_box)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.retranslateUi(SettingsFrame)
        self.telescope_check_box.toggled.connect(self.telescope_settings_button.setEnabled)
        self.guider_check_box.toggled.connect(self.guider_settings_button.setEnabled)
        self.camera_check_box.toggled.connect(self.camera_settings_button.setEnabled)
        self.filter_wheel_check_box.toggled.connect(self.filter_wheel_settings_button.setEnabled)
        self.focuser_check_box.toggled.connect(self.focuser_settings_button.setEnabled)

        self.astap_location_button.setDefault(False)


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
        self.observer_group_box.setTitle(QCoreApplication.translate("SettingsFrame", u"Observer", None))
        self.observer_name_label.setText(QCoreApplication.translate("SettingsFrame", u"Name", None))
        self.observer_telescope_label.setText(QCoreApplication.translate("SettingsFrame", u"Telescope", None))
        self.observer_camera_label.setText(QCoreApplication.translate("SettingsFrame", u"Camera", None))
        self.filters_group_box.setTitle(QCoreApplication.translate("SettingsFrame", u"Filters", None))
        self.plate_solving_group_box.setTitle(QCoreApplication.translate("SettingsFrame", u"Plate solving", None))
        self.astap_radio.setText(QCoreApplication.translate("SettingsFrame", u"ASTAP", None))
        self.astap_location_button.setText(QCoreApplication.translate("SettingsFrame", u"Browse...", None))
        self.label.setText(QCoreApplication.translate("SettingsFrame", u"<html><head/><body><p>ASTAP is a free stacking and astrometric solver (plate solver) program. It has a powerful FITS viewer and the native astrometric solver can be used by Ecliptic or other imaging programs to synchronise the mount based on an image taken.</p><p><a href=\"http://www.hnsky.org/astap.htm\"><span style=\" text-decoration: underline; color:#007af4;\">http://www.hnsky.org/astap.htm</span></a></p></body></html>", None))
        self.search_radius_label.setText(QCoreApplication.translate("SettingsFrame", u"Search radius", None))
        self.search_radius_spin_box.setSuffix(QCoreApplication.translate("SettingsFrame", u"\u00b0", None))
        self.downsample_label.setText(QCoreApplication.translate("SettingsFrame", u"Downsample", None))
        self.downsample_combo_box.setItemText(0, QCoreApplication.translate("SettingsFrame", u"Auto", None))
        self.downsample_combo_box.setItemText(1, QCoreApplication.translate("SettingsFrame", u"1", None))
        self.downsample_combo_box.setItemText(2, QCoreApplication.translate("SettingsFrame", u"2", None))
        self.downsample_combo_box.setItemText(3, QCoreApplication.translate("SettingsFrame", u"3", None))
        self.downsample_combo_box.setItemText(4, QCoreApplication.translate("SettingsFrame", u"4", None))

        self.plate_solve_debug_check_box.setText(QCoreApplication.translate("SettingsFrame", u"Debug", None))
    # retranslateUi

