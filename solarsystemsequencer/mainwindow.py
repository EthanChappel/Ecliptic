import json
import os
import sys
import threading
from datetime import datetime
from typing import List, Dict
import cv2
import zwoasi as asi
from PIL import Image, ImageQt
from PySide2 import QtCore, QtGui, QtWidgets
import appglobals
import connectcamera
import zwosettings
import guiderparameters
from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QTableWidgetItem
from astropy.time import Time
from astropy.coordinates import get_body
from ui.ui_mainwindow import Ui_MainWindow
from ui.delegates import QTimeEditItemDelegate, QComboBoxItemDelegate, QSpinBoxItemDelegate

if sys.platform.startswith("win"):
    from equipment import ascom


EXPOSURE_UNIT = "ms"
GAIN_UNIT = "e/adu"
INTEGRATION_UNIT = "s"
CUTOFF_UNIT = "nm"


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.camera_thread = None
        self.guider_thread = None

        self.menu = QtWidgets.QMenu()
        self.status_coords_label = QtWidgets.QLabel()
        self.setupUi(self)

        self.camera_settings_frame = zwosettings.ZWOSettings()
        self.camera_settings_action = QtWidgets.QWidgetAction(None)
        self.camera_settings_menu = QtWidgets.QMenu()
        self.camera_settings_menu.addAction(self.savelocation_action)
        self.camera_settings_btn.setMenu(self.camera_settings_menu)

        self.guider_settings_frame = zwosettings.ZWOSettings()
        self.guider_parameters_frame = guiderparameters.GuiderParameters()
        self.guider_settings_action = QtWidgets.QWidgetAction(None)
        self.guider_settings_action.setDefaultWidget(self.guider_settings_frame)
        self.guider_parameters_action = QtWidgets.QWidgetAction(None)
        self.guider_parameters_action.setDefaultWidget(self.guider_parameters_frame)
        self.guider_menu = QtWidgets.QMenu()
        self.guider_menu.addAction(self.guider_parameters_action)
        self.guider_settings_btn.setMenu(self.guider_menu)

        self.row_count = self.schedule_table.rowCount()

        self.mountmodes_tuple = ("Stop", "Home")

        # Models for schedule table columns.
        self.target_list_model = QStringListModel()
        self.filter_list_model = QStringListModel()

        # Create Delegates for columns in schedule table.
        self.time_delegate = QTimeEditItemDelegate(self)
        self.target_delegate = QComboBoxItemDelegate(self, self.target_list_model)
        self.filter_delegate = QComboBoxItemDelegate(self, self.filter_list_model)
        self.exposure_delegate = QSpinBoxItemDelegate(self, suffix=EXPOSURE_UNIT)
        self.gain_delegate = QSpinBoxItemDelegate(self, suffix=GAIN_UNIT)
        self.integration_delegate = QSpinBoxItemDelegate(self, suffix=INTEGRATION_UNIT)

        # Create Delegates for columns in filters table.
        self.position_delegate = QSpinBoxItemDelegate(self)
        self.lower_cutoff_delegate = QSpinBoxItemDelegate(self, 0, 2000, CUTOFF_UNIT)
        self.upper_cutoff_delegate = QSpinBoxItemDelegate(self, 0, 2000, CUTOFF_UNIT)

        if sys.platform.startswith("win"):
            asi.init(str(sys.path[0]) + "\\lib\\ASICamera2.dll")

        self.setup_gui()

    def setup_gui(self):
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        self.tabifyDockWidget(self.schedule_dockwidget, self.guider_dockwidget)
        self.tabifyDockWidget(self.guider_dockwidget, self.camera_dockwidget)
        self.tabifyDockWidget(self.camera_dockwidget, self.filters_dockwidget)
        self.tabifyDockWidget(self.filters_dockwidget, self.settings_dockwidget)
        self.schedule_dockwidget.raise_()
        self.camera_dockwidget.setVisible(False)
        self.guider_dockwidget.setVisible(False)

        self.slewstop_button.clicked.connect(self.goto_target)
        self.telescope_action.toggled.connect(self.connect_telescope)
        self.camera_action.toggled.connect(self.connect_camera)
        self.guider_action.toggled.connect(self.connect_guider)
        self.focuser_action.toggled.connect(self.connect_focuser)
        self.wheel_action.toggled.connect(self.connect_filters)

        self.scope_settings_btn.clicked.connect(self.setup_telescope)
        self.ascomcamerasettings_action.triggered.connect(self.setup_camera)
        self.ascomguidersettings_action.triggered.connect(self.setup_guider)
        self.focuser_settings_btn.clicked.connect(self.setup_focuser)
        self.wheel_settings_btn.clicked.connect(self.setup_filterwheel)

        # Connects pressed event that moves mount to the directional buttons
        self.slewnorth_button.pressed.connect(
            lambda: appglobals.telescope.move_axis(1, self.mount_trackrate_spin.cleanText())
        )
        self.slewnorth_button.pressed.connect(
            lambda: appglobals.telescope.move_axis(1, self.mount_trackrate_spin.cleanText())
        )
        self.sleweast_button.pressed.connect(
            lambda: appglobals.telescope.move_axis(0, self.mount_trackrate_spin.cleanText())
        )
        self.slewsouth_button.pressed.connect(
            lambda: appglobals.telescope.move_axis(1, -1 * float(self.mount_trackrate_spin.cleanText()))
        )
        self.slewwest_button.pressed.connect(
            lambda: appglobals.telescope.move_axis(0, -1 * float(self.mount_trackrate_spin.cleanText()))
        )
        self.slewnortheast_button.pressed.connect(
            lambda: self.slew_diagonal(self.mount_trackrate_spin.cleanText(), self.mount_trackrate_spin.cleanText())
        )
        self.slewsoutheast_button.pressed.connect(
            lambda: self.slew_diagonal(
                self.mount_trackrate_spin.cleanText(),
                -1 * float(self.mount_trackrate_spin.cleanText())
            )
        )
        self.slewsouthwest_button.pressed.connect(
            lambda: self.slew_diagonal(
                -1 * float(self.mount_trackrate_spin.cleanText()),
                -1 * float(self.mount_trackrate_spin.cleanText())
            )
        )
        self.slewnorthwest_button.pressed.connect(
            lambda: self.slew_diagonal(
                -1 * float(self.mount_trackrate_spin.cleanText()),
                self.mount_trackrate_spin.cleanText()
            )
        )

        # Connects clicked event that stops mount to the directional buttons
        self.slewnorth_button.released.connect(lambda: appglobals.telescope.move_axis(1, 0.0))
        self.sleweast_button.released.connect(lambda: appglobals.telescope.move_axis(0, 0.0))
        self.slewsouth_button.released.connect(lambda: appglobals.telescope.move_axis(1, 0.0))
        self.slewwest_button.released.connect(lambda: appglobals.telescope.move_axis(0, 0.0))
        self.slewnortheast_button.released.connect(lambda: self.slew_diagonal(0.0, 0.0))
        self.slewsoutheast_button.released.connect(lambda: self.slew_diagonal(0.0, 0.0))
        self.slewsouthwest_button.released.connect(lambda: self.slew_diagonal(0.0, 0.0))
        self.slewnorthwest_button.released.connect(lambda: self.slew_diagonal(0.0, 0.0))

        self.goto_button.clicked.connect(self.goto_target)

        self.guider_loop_button.clicked.connect(self.guider_loop)
        self.camera_loop_button.clicked.connect(self.camera_loop)

        self.guider_start_button.clicked.connect(self.guider_loop)
        self.camera_capture_button.clicked.connect(self.camera_loop)

        # Connect functions to addrow_button and removerow_button
        self.addrow_button.clicked.connect(self.add_schedule_row)
        self.removerow_button.clicked.connect(self.remove_schedule_row)

        # Connect functions to actions
        self.location_action.triggered.connect(lambda: self.settings_dockwidget.raise_())

        # Add targets to object_combobox
        self.object_combobox.addItems(self.mountmodes_tuple)
        self.object_combobox.addItems(appglobals.targets_tuple)

        # Set label to show latitude and longitude and show it on status bar
        self.status_coords_label.setText(
            "Latitude: %d°%d\'%d\", Longitude: %d°%d\'%d\"" % (
                appglobals.location["Latitude"][0],
                appglobals.location["Latitude"][1],
                appglobals.location["Latitude"][2],
                appglobals.location["Longitude"][0],
                appglobals.location["Longitude"][1],
                appglobals.location["Longitude"][2]
            )
        )
        self.statusbar.addWidget(self.status_coords_label)

        # Fill location widgets with saved values.
        self.lat_d_spin.setValue(appglobals.location["Latitude"][0])
        self.long_d_spin.setValue(appglobals.location["Longitude"][0])
        self.lat_m_spin.setValue(appglobals.location["Latitude"][1])
        self.long_m_spin.setValue(appglobals.location["Longitude"][1])
        self.lat_s_spin.setValue(appglobals.location["Latitude"][2])
        self.long_s_spin.setValue(appglobals.location["Longitude"][2])

        # Save location when changed.
        self.lat_d_spin.valueChanged.connect(self.location_set)
        self.lat_m_spin.valueChanged.connect(self.location_set)
        self.lat_s_spin.valueChanged.connect(self.location_set)
        self.long_d_spin.valueChanged.connect(self.location_set)
        self.long_m_spin.valueChanged.connect(self.location_set)
        self.long_s_spin.valueChanged.connect(self.location_set)

        # Allow table headers to fit schedule_table
        self.schedule_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.filter_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Set schedule_dateedit to today
        self.schedule_dateedit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.focuser_position_spinbox.setKeyboardTracking(False)
        self.focuser_position_spinbox.lineEdit().returnPressed.connect(self.move_focuser)
        self.focuser_position_spinbox.valueChanged.connect(self.move_focuser)
        self.temp_checkbox.stateChanged.connect(self.temp_comp)

        # Add targets to position_combobox
        self.camera_filter_combobox.addItem("None")
        for f in appglobals.filters:
            self.position_combobox.addItem(f.get("Name"))
            self.camera_filter_combobox.addItem(f["Name"])

        self.position_combobox.lineEdit().returnPressed.connect(self.change_filter)
        self.position_combobox.currentIndexChanged.connect(self.change_filter)

        self.temp_checkbox.setVisible(False)

        self.addrow_button_2.clicked.connect(self.add_filter_row)
        self.removerow_button_2.clicked.connect(self.remove_filter_row)

        date = self.schedule_dateedit.text()
        self.load_schedule(date)
        self.load_filters(appglobals.filters)

        self.schedule_dateedit.dateChanged.connect(lambda: self.load_schedule(str(self.schedule_dateedit.text())))

        self.schedule_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.filter_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.camera_exposure_spinbox.valueChanged.connect(self.set_camera_exposure)
        self.camera_exposure_slider.valueChanged.connect(self.set_camera_exposure)
        self.camera_gain_spinbox.valueChanged.connect(self.set_camera_gain)
        self.camera_gain_slider.valueChanged.connect(self.set_camera_gain)

        self.guider_exposure_spinbox.valueChanged.connect(self.set_guider_exposure)
        self.guider_exposure_slider.valueChanged.connect(self.set_guider_exposure)
        self.guider_gain_spinbox.valueChanged.connect(self.set_guider_gain)
        self.guider_gain_slider.valueChanged.connect(self.set_guider_gain)

        self.savelocation_action.triggered.connect(self.change_camera_save_dir)

        # Set the choices for the targets column.
        self.target_list_model.setStringList(self.mountmodes_tuple + appglobals.targets_tuple)

        # Set the choices for the filters column.
        filter_names = []
        for f in appglobals.filters:
            filter_names.append(f["Name"])
        self.filter_list_model.setStringList(filter_names)

        # Set item delegates for columns in schedule table.
        self.schedule_table.setItemDelegateForColumn(0, self.time_delegate)
        self.schedule_table.setItemDelegateForColumn(1, self.target_delegate)
        self.schedule_table.setItemDelegateForColumn(2, self.filter_delegate)
        self.schedule_table.setItemDelegateForColumn(3, self.exposure_delegate)
        self.schedule_table.setItemDelegateForColumn(4, self.gain_delegate)
        self.schedule_table.setItemDelegateForColumn(5, self.integration_delegate)

        self.filter_table.setItemDelegateForColumn(2, self.position_delegate)
        self.filter_table.setItemDelegateForColumn(3, self.lower_cutoff_delegate)
        self.filter_table.setItemDelegateForColumn(4, self.upper_cutoff_delegate)

        # Save whenever cell is changed.
        self.schedule_table.itemChanged.connect(self.save_schedule)
        self.filter_table.itemChanged.connect(self.save_filters)

    def add_schedule_row(self):
        """Add row in schedule_table."""
        self.row_count = self.schedule_table.rowCount()
        self.schedule_table.insertRow(self.row_count)

    def remove_schedule_row(self):
        """Remove selected rows from schedule_table."""
        index_list = []
        date = self.schedule_dateedit.text()
        for model_index in self.schedule_table.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.schedule_table.removeRow(index.row())
            del appglobals.schedule[date][index.row()]
        self.save_schedule()

    def save_schedule(self):
        """Save contents of schedule_table into schedule.json."""
        schedule_list = []
        for row in range(self.schedule_table.rowCount()):
            schedule_dict = {}
            for col in range(self.schedule_table.columnCount()):
                header = str(self.schedule_table.horizontalHeaderItem(col).text())
                item = self.schedule_table.item(row, col)
                value = None

                # Save existing items with numeric strings as integers.
                if item is None:
                    pass
                elif col > 2 and item.text() not in ("", "None"):
                    value = int(item.text())
                elif isinstance(item.text(), str) and item.text() not in ("", "None"):
                    value = item.text()

                schedule_dict.update({header: value})
            schedule_list.append(schedule_dict)
            appglobals.schedule.update({self.schedule_dateedit.text(): schedule_list})
        with open("schedule.json", "w") as f:
            json.dump(appglobals.schedule, f, indent=4)

    def load_schedule(self, date: str):
        """Load contents of schedule.json into schedule_table."""
        self.schedule_table.setRowCount(0)
        if date in appglobals.schedule:
            count = 0
            for f in appglobals.schedule[date]:
                self.add_schedule_row()

                self.schedule_table.setItem(count, 0, QTableWidgetItem(f["Time"]))
                self.schedule_table.setItem(count, 1, QTableWidgetItem(f["Target"]))
                self.schedule_table.setItem(count, 2, QTableWidgetItem(f["Filter"]))
                self.schedule_table.setItem(count, 3, QTableWidgetItem(str(f["Exposure"])))
                self.schedule_table.setItem(count, 4, QTableWidgetItem(str(f["Gain"])))
                self.schedule_table.setItem(count, 5, QTableWidgetItem(str(f["Integration"])))
                count += 1

    def add_filter_row(self):
        """Add row in filter_table."""
        self.row_count = self.filter_table.rowCount()
        self.filter_table.insertRow(self.row_count)

    def remove_filter_row(self):
        """Remove selected rows from filter_table."""
        index_list = []
        for model_index in self.filter_table.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.filter_table.removeRow(index.row())
        self.save_filters()

    def save_filters(self):
        """Save contents of filter_table into filters.json."""
        if os.path.exists("filters.json"):
            os.remove("filters.json")
        filter_list = []
        for row in range(self.filter_table.rowCount()):
            filter_dict = {}
            for col in range(self.filter_table.columnCount()):
                header = str(self.filter_table.horizontalHeaderItem(col).text())
                item = self.filter_table.item(row, col)
                value = None

                # Save existing items with numeric strings as integers.
                if item is None:
                    pass
                elif col > 1 and item.text() not in ("", "None"):
                    value = int(item.text())
                elif isinstance(item.text(), str) and item.text() not in ("", "None"):
                    value = item.text()
                filter_dict.update({header: value})
            filter_list.append(filter_dict)
        with open("filters.json", "a") as f:
            json.dump(filter_list, f, indent=0)
        with open("filters.json", "r") as f:
            appglobals.filters = json.load(f)

        # Update filter model
        filter_names = []
        for f in appglobals.filters:
            filter_names.append(f["Name"])
        self.filter_list_model.setStringList(filter_names)

        self.position_combobox.blockSignals(True)
        text = self.position_combobox.currentText()
        text2 = self.camera_filter_combobox.currentText()
        self.position_combobox.clear()
        self.camera_filter_combobox.clear()
        self.camera_filter_combobox.addItem("None")
        for f in appglobals.filters:
            self.camera_filter_combobox.addItem(f["Name"])
            self.position_combobox.addItem(f["Name"])
        index = self.position_combobox.findText(text)
        self.position_combobox.setCurrentIndex(index)
        self.position_combobox.blockSignals(False)
        index = self.position_combobox.findText(text2)
        self.position_combobox.setCurrentIndex(index)

    def load_filters(self, filters: List[Dict[str, str]]):
        """Load contents of filters.json into filter_table."""
        count = 0
        for f in filters:
            self.add_filter_row()

            self.filter_table.setItem(count, 0, QTableWidgetItem(f["Name"]))
            self.filter_table.setItem(count, 1, QTableWidgetItem(f["Brand"]))
            self.filter_table.setItem(count, 2, QTableWidgetItem(str(f["Wheel Position"])))
            self.filter_table.setItem(count, 3, QTableWidgetItem(str(f["Lower Cutoff"])))
            self.filter_table.setItem(count, 4, QTableWidgetItem(str(f["Upper Cutoff"])))

            count += 1

    def location_set(self):
        """Set observing location."""
        appglobals.location["Latitude"] = [
            self.lat_d_spin.value(), self.lat_m_spin.value(), self.lat_s_spin.value()
        ]
        appglobals.location["Longitude"] = [
            self.long_d_spin.value(), self.long_m_spin.value(), self.long_s_spin.value()
        ]

        if os.path.exists("location.json"):
            os.remove("location.json")
        with open("location.json", "a") as f:
            json.dump(appglobals.location, f, indent=0)
        self.status_coords_label.setText(
            "Latitude: %d°%d\'%d\", Longitude: %d°%d\'%d\"" % (
                appglobals.location["Latitude"][0],
                appglobals.location["Latitude"][1],
                appglobals.location["Latitude"][2],
                appglobals.location["Longitude"][0],
                appglobals.location["Longitude"][1],
                appglobals.location["Longitude"][2]
            )
        )

    @staticmethod
    def connect_fail_dialog(name: str):
        """Notify users if connection to equipment fails."""
        messagebox = QtWidgets.QMessageBox()
        messagebox.setIcon(QtWidgets.QMessageBox.Warning)
        messagebox.setWindowTitle("Solar System Sequencer - Connection Failed")
        messagebox.setText("{} failed to connect.".format(name))
        messagebox.exec_()

    def connect_telescope(self):
        if self.mount_group.isChecked():
            name = "The telescope"
            try:
                appglobals.telescope = ascom.Telescope()
                self.telescope_settings()
                name = appglobals.telescope.name_()
                self.telescope_name_label.setText(name)
            except Exception as e:
                print(e)
                self.mount_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.mount_group.isChecked():
            try:
                appglobals.telescope.disconnect()
                appglobals.telescope.dispose()
            except AttributeError as e:
                print(e)
            appglobals.telescope = None
            self.telescope_name_label.setText("Not Connected")

    def setup_telescope(self):
        appglobals.telescope.disconnect()
        appglobals.telescope.setup_dialog()
        appglobals.telescope.connect()
        self.telescope_settings()

    def telescope_settings(self):
        if not appglobals.telescope.can_slew_eq():
            messagebox = QtWidgets.QMessageBox()
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setText("ASCOM Telescopes that can't accept equatorial coordinates are not supported!")
            messagebox.exec_()
            self.telescope_action.setChecked(False)

    def goto_target(self):
        goto_thread = threading.Thread(target=self.goto_target_thread)
        goto_thread.start()

    def goto_target_thread(self):
        if self.object_combobox.currentText() == "Home":
            appglobals.telescope.home()
        elif self.object_combobox.currentText() == "Stop" or self.sender() is self.slewstop_button:
            appglobals.telescope.stop_tracking()
        else:
            body = get_body(self.object_combobox.currentText().lower(), Time.now())
            appglobals.telescope.goto(body.ra.hour, body.dec.degree)

    @staticmethod
    def slew_diagonal(rate1: float, rate2: float):
        appglobals.telescope.move_axis(0, rate1)
        appglobals.telescope.move_axis(1, rate2)

    def connect_guider(self):
        if self.guider_group.isChecked():
            guider_dialog = connectcamera.ConnectCamera()
            guider_dialog.exec_()
            name = "The guider"
            try:
                if not guider_dialog.asi_selected and guider_dialog.accepted:
                    appglobals.guider = ascom.Camera()
                    values = self.camera_settings(appglobals.guider)
                    name = appglobals.guider.name_()
                    self.guider_name_label.setText(name)
                    self.guider_menu.addAction(self.ascomguidersettings_action)
                elif guider_dialog.asi_selected and guider_dialog.accepted:
                    appglobals.guider = asi.Camera(asi.list_cameras().index(guider_dialog.asi_camera))
                    values = self.camera_settings(appglobals.guider)
                    self.guider_settings_frame.set_camera(appglobals.guider)
                    self.guider_name_label.setText(guider_dialog.asi_camera)
                    self.guider_menu.addAction(self.guider_settings_action)
                else:
                    raise Exception
                self.setup_guider_controls(values)
            except Exception as e:
                print(e)
                self.guider_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.guider_group.isChecked():
            try:
                if type(appglobals.guider) is ascom.Camera:
                    self.guider_menu.removeAction(self.ascomguidersettings_action)
                    appglobals.guider.disconnect()
                    appglobals.guider.dispose()
                elif type(appglobals.guider) is asi.Camera:
                    self.guider_menu.removeAction(self.guider_settings_action)
                    appglobals.guider.close()
            except AttributeError as e:
                print(e)
            finally:
                appglobals.guider = None
                self.guider_settings_frame.set_camera(appglobals.guider)
                self.guider_name_label.setText("Not Connected")

    def setup_guider(self):
        appglobals.guider.disconnect()
        appglobals.guider.setup_dialog()
        appglobals.guider.connect()
        self.setup_guider_controls(self.camera_settings(appglobals.guider))

    def set_guider_exposure(self):
        if type(appglobals.guider) is asi.Camera:
            exp_us = int(self.guider_exposure_spinbox.cleanText()) * 1000
            appglobals.guider.set_control_value(asi.ASI_EXPOSURE, exp_us)

    def set_guider_gain(self):
        if type(appglobals.guider) is asi.Camera:
            gain = int(self.guider_gain_spinbox.cleanText())
            appglobals.guider.set_control_value(asi.ASI_GAIN, gain)

    def setup_guider_controls(self, values):
        if "Gain" in values:
            self.guider_gain_spinbox.setMinimum(values["Gain"]["Min"])
            self.guider_gain_spinbox.setMaximum(values["Gain"]["Max"])
            self.guider_gain_slider.setMinimum(values["Gain"]["Min"])
            self.guider_gain_slider.setMaximum(values["Gain"]["Max"])
            self.guider_gain_spinbox.setValue(values["Gain"]["Current"])
        else:
            self.guider_gain_label.setEnabled(False)
            self.guider_gain_spinbox.setEnabled(False)
            self.guider_gain_slider.setEnabled(False)

        if "Exposure" in values:
            self.guider_exposure_spinbox.setMinimum(values["Exposure"]["Min"])
            self.guider_exposure_spinbox.setMaximum(values["Exposure"]["Max"])
            self.guider_exposure_slider.setMinimum(values["Exposure"]["Min"])
            self.guider_exposure_slider.setMaximum(values["Exposure"]["Max"])
            self.guider_exposure_spinbox.setValue(values["Exposure"]["Current"])
        else:
            self.guider_exposure_label.setEnabled(False)
            self.guider_exposure_spinbox.setEnabled(False)
            self.guider_exposure_slider.setEnabled(False)

        self.guider_settings_frame.setup_controls(values)

    def guider_loop(self):
        if self.guider_loop_button.isChecked():
            if self.guider_start_button.isChecked():
                self.guider_thread = threading.Thread(target=self.guider_preview)  # To be implemented
            else:
                self.guider_thread = threading.Thread(target=self.guider_preview)
            self.guider_thread.daemon = True
            self.guider_thread.start()

    def guider_preview(self):
        if type(appglobals.guider) is ascom.Camera:
            while self.guider_loop_button.isChecked():  # and not self.camera_capture_button.isChecked():
                exp_sec = float(self.guider_exposure_spinbox.cleanText()) / 1000
                image = appglobals.guider.capture(exp_sec, True)
                image = Image.fromarray(image)
                pix = ImageQt.toqpixmap(image)
                self.guider_preview_label.setPixmap(pix)
        else:
            appglobals.guider.start_video_capture()
            while self.guider_loop_button.isChecked():
                timeout = int(self.guider_exposure_spinbox.cleanText()) * 2 + 500
                image = appglobals.guider.capture_video_frame(timeout=timeout)
                image = Image.fromarray(image)
                pix = ImageQt.toqpixmap(image)
                self.guider_preview_label.setPixmap(pix)
        self.guider_preview_label.clear()

    def connect_camera(self):
        if self.camera_group.isChecked():
            name = "The camera"
            camera_dialog = connectcamera.ConnectCamera()
            camera_dialog.exec_()
            try:
                if not camera_dialog.asi_selected and camera_dialog.accepted:
                    appglobals.camera = ascom.Camera()
                    values = self.camera_settings(appglobals.camera)
                    name = appglobals.camera.name_()
                    self.camera_name_label.setText(name)
                    self.camera_settings_menu.insertAction(self.savelocation_action, self.ascomcamerasettings_action)
                elif camera_dialog.asi_selected and camera_dialog.accepted:
                    appglobals.camera = asi.Camera(asi.list_cameras().index(camera_dialog.asi_camera))
                    values = self.camera_settings(appglobals.camera)
                    self.camera_settings_frame.set_camera(appglobals.camera)
                    self.camera_name_label.setText(camera_dialog.asi_camera)
                    self.camera_settings_action.setDefaultWidget(self.camera_settings_frame)
                    self.camera_settings_menu.insertAction(self.savelocation_action, self.camera_settings_action)
                else:
                    raise Exception
                self.setup_camera_controls(values)
            except Exception as e:
                print(e)
                self.camera_group.setChecked(False)
                self.connect_fail_dialog(name)

        elif not self.camera_group.isChecked():
            try:
                if type(appglobals.camera) is ascom.Camera:
                    self.camera_settings_menu.removeAction(self.ascomcamerasettings_action)
                    appglobals.camera.disconnect()
                    appglobals.camera.dispose()
                elif type(appglobals.camera) is asi.Camera:
                    self.camera_settings_menu.removeAction(self.camera_settings_action)
                    appglobals.camera.close()
            except AttributeError as e:
                print(e)
            finally:
                appglobals.camera = None
                self.camera_settings_frame.set_camera(appglobals.camera)
                self.camera_name_label.setText("Not Connected")

    def setup_camera_controls(self, values):
        # TODO: Test these statements with more cameras that support different features
        if "Gain" in values:
            self.camera_gain_spinbox.setMinimum(values["Gain"]["Min"])
            self.camera_gain_spinbox.setMaximum(values["Gain"]["Max"])
            self.camera_gain_slider.setMinimum(values["Gain"]["Min"])
            self.camera_gain_slider.setMaximum(values["Gain"]["Max"])
            self.camera_gain_spinbox.setValue(values["Gain"]["Current"])
        else:
            self.camera_gain_label.setEnabled(False)
            self.camera_gain_spinbox.setEnabled(False)
            self.camera_gain_slider.setEnabled(False)

        if "Exposure" in values:
            self.camera_exposure_spinbox.setMinimum(values["Exposure"]["Min"])
            self.camera_exposure_spinbox.setMaximum(values["Exposure"]["Max"])
            self.camera_exposure_slider.setMinimum(values["Exposure"]["Min"])
            self.camera_exposure_slider.setMaximum(values["Exposure"]["Max"])
            self.camera_exposure_spinbox.setValue(values["Exposure"]["Current"])
        else:
            self.camera_exposure_label.setEnabled(False)
            self.camera_exposure_spinbox.setEnabled(False)
            self.camera_exposure_slider.setEnabled(False)

        self.camera_settings_frame.setup_controls(values)

    def setup_camera(self):
        appglobals.camera.disconnect()
        appglobals.camera.setup_dialog()
        appglobals.camera.connect()
        self.setup_camera_controls(self.camera_settings(appglobals.camera))

    def camera_settings(self, camera):
        values = {}
        if type(camera) is ascom.Camera:
            values.update({"Gain": {"Min": camera.gain_min(), "Max": camera.gain_max(), "Current": camera.gain()}})
            values.update({"Exposure": {"Min": camera.exposure_min() * 1000,
                                        "Max": camera.exposure_max() * 1000,
                                        "Current": camera.exposure_min() * 1000}})  # No current value in ASCOM

        elif type(camera) is asi.Camera:
            controls = camera.get_controls()
            if controls["Gain"]["IsAutoSupported"]:
                values.update({"Gain": {"Min": controls["Gain"]["MinValue"],
                                        "Max": controls["Gain"]["MaxValue"],
                                        "Current": camera.get_control_value(asi.ASI_GAIN)[0]}})

            if controls["Exposure"]["IsAutoSupported"]:
                values.update({"Exposure": {"Min": controls["Exposure"]["MinValue"] / 1000,
                                            "Max": controls["Exposure"]["MaxValue"] / 1000,
                                            "Current": camera.get_control_value(asi.ASI_EXPOSURE)[0] / 1000}})

            if controls["Gamma"]["IsAutoSupported"]:
                values.update({"Gamma": {"Min": controls["Gamma"]["MinValue"],
                                         "Max": controls["Gamma"]["MaxValue"],
                                         "Current": camera.get_control_value(asi.ASI_GAMMA)[0]}})

            if controls["Brightness"]["IsAutoSupported"]:
                values.update({"Brightness": {"Min": controls["Brightness"]["MinValue"],
                                              "Max": controls["Brightness"]["MaxValue"],
                                              "Current": camera.get_control_value(asi.ASI_BRIGHTNESS)[0]}})

            if controls["BandWidth"]["IsAutoSupported"]:
                values.update({"Bandwidth": {"Min": controls["BandWidth"]["MinValue"],
                                             "Max": controls["BandWidth"]["MaxValue"],
                                             "Current": camera.get_control_value(asi.ASI_BANDWIDTHOVERLOAD)[0]}})

            if controls["Flip"]["IsAutoSupported"]:
                values.update({"Flip": {"Min": controls["Flip"]["MinValue"],
                                        "Max": controls["Flip"]["MaxValue"],
                                        "Current": camera.get_control_value(asi.ASI_FLIP)[0]}})

            if controls["HighSpeedMode"]["IsAutoSupported"]:
                values.update({"High Speed": {"Min": controls["HighSpeedMode"]["MinValue"],
                                              "Max": controls["HighSpeedMode"]["MaxValue"],
                                              "Current": camera.get_control_value(asi.ASI_HIGH_SPEED_MODE)[0]}})

            if controls["Temperature"]["IsAutoSupported"]:
                values.update({"Temperature": {"Min": controls["Temperature"]["MinValue"],
                                               "Max": controls["Temperature"]["MaxValue"],
                                               "Current": camera.get_control_value(asi.ASI_TARGET_TEMP)[0]}})

            if camera.get_camera_property()["IsColorCam"]:
                if controls["WB_R"]["IsAutoSupported"]:
                    values.update({"Red": {"Min": controls["WB_R"]["MinValue"],
                                           "Max": controls["WB_R"]["MaxValue"],
                                           "Current": camera.get_control_value(asi.ASI_WB_R)[0]}})

                if controls["WB_B"]["IsAutoSupported"]:
                    values.update({"Blue": {"Min": controls["WB_B"]["MinValue"],
                                            "Max": controls["WB_B"]["MaxValue"],
                                            "Current": camera.get_control_value(asi.ASI_WB_B)[0]}})

            if "HardwareBin" in controls:
                # TODO: Determine if HardwareBin is correlated with color cameras
                if controls["HardwareBin"]["IsAutoSupported"]:
                    values.update({"Hardware Bin": {"Min": controls["HardwareBin"]["MinValue"],
                                                    "Max": controls["HardwareBin"]["MaxValue"],
                                                    "Current": camera.get_control_value(asi.ASI_HARDWARE_BIN)[0]}})

            if "Mono bin" in controls:
                # TODO: Determine if Mono bin is correlated with color cameras
                if controls["Mono bin"]["IsAutoSupported"]:
                    values.update({"Mono Bin": {"Min": controls["Mono bin"]["MinValue"],
                                                "Max": controls["Mono bin"]["MaxValue"],
                                                "Current": camera.get_control_value(asi.ASI_MONO_BIN)[0]}})

        return values

    def set_camera_exposure(self):
        if type(appglobals.camera) is asi.Camera:
            exp_us = int(self.camera_exposure_spinbox.cleanText()) * 1000
            appglobals.camera.set_control_value(asi.ASI_EXPOSURE, exp_us)

    def set_camera_gain(self):
        if type(appglobals.camera) is asi.Camera:
            gain = int(self.camera_gain_spinbox.cleanText())
            appglobals.camera.set_control_value(asi.ASI_GAIN, gain)

    def camera_loop(self):
        if self.camera_loop_button.isChecked():
            if self.camera_capture_button.isChecked():
                self.camera_thread = threading.Thread(target=self.camera_record)
            else:
                self.camera_thread = threading.Thread(target=self.camera_preview)
            self.camera_thread.daemon = True
            self.camera_thread.start()

    def camera_preview(self):
        if type(appglobals.camera) is ascom.Camera:
            while self.camera_loop_button.isChecked() and not self.camera_capture_button.isChecked():
                exp_sec = float(self.camera_exposure_spinbox.cleanText()) / 1000
                image = appglobals.camera.capture(exp_sec, True)
                image = Image.fromarray(image)
                pix = ImageQt.toqpixmap(image)
                self.camera_preview_label.setPixmap(pix)
        else:
            appglobals.camera.start_video_capture()
            while self.camera_loop_button.isChecked():
                timeout = int(self.camera_exposure_spinbox.cleanText()) * 2 + 500
                image = appglobals.camera.capture_video_frame(timeout=timeout)
                image = Image.fromarray(image)
                pix = ImageQt.toqpixmap(image)
                self.camera_preview_label.setPixmap(pix)
        self.camera_preview_label.clear()

    def camera_record(self):
        name_format = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        avi_name = "{}/{}.avi".format(appglobals.settings["Save Directory"], name_format)
        if type(appglobals.camera) is ascom.Camera:
            out = cv2.VideoWriter(avi_name, -1, 20.0, (appglobals.camera.num_x(), appglobals.camera.num_y()), False)
            while self.camera_capture_button.isChecked():
                exp_sec = float(self.camera_exposure_spinbox.cleanText()) / 1000
                image = appglobals.camera.capture(exp_sec, True)
                out.write(image)
                image = Image.fromarray(image)
                pix = ImageQt.toqpixmap(image)
                self.camera_preview_label.setPixmap(pix)
        else:
            print(0)
            width = appglobals.camera.get_camera_property()["MaxWidth"]
            height = appglobals.camera.get_camera_property()["MaxHeight"]
            out = cv2.VideoWriter(avi_name, -1, 20.0, (width, height), False)
            while self.camera_capture_button.isChecked():
                timeout = int(self.camera_exposure_spinbox.cleanText()) * 2 + 500
                image = appglobals.camera.capture_video_frame(timeout=timeout)
                out.write(image)
                image = Image.fromarray(image)
                pix = ImageQt.toqpixmap(image)
                self.camera_preview_label.setPixmap(pix)
        out.release()
        if os.path.getsize(avi_name) == 0:
            os.remove(avi_name)

    def save_settings(self):
        """Save application settings into settings.json."""
        if os.path.exists("settings.json"):
            os.remove("settings.json")

        with open("settings.json", "a") as f:
            json.dump(appglobals.settings, f, indent=4)

    def change_camera_save_dir(self):
        camera_dir_dialog = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory",
                                                                       appglobals.settings["Save Directory"])
        if str(camera_dir_dialog) == "":
            pass
        else:
            appglobals.settings["Save Directory"] = str(camera_dir_dialog)
            self.save_settings()

    def connect_focuser(self):
        if self.focuser_group.isChecked():
            name = "The focuser"
            try:
                appglobals.focuser = ascom.Focuser()
                self.focuser_settings()
                name = appglobals.focuser.name_()
                self.focuser_name_label.setText(name)
            except Exception as e:
                print(e)
                self.focuser_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.focuser_group.isChecked():
            try:
                self.temp_checkbox.setVisible(False)
                self.temp_checkbox.setChecked(False)
                appglobals.focuser.disconnect()
                appglobals.focuser.dispose()
            except AttributeError as e:
                print(e)
            finally:
                appglobals.focuser = None
                self.focuser_name_label.setText("Not Connected")

    def setup_focuser(self):
        appglobals.focuser.disconnect()
        appglobals.focuser.setup_dialog()
        appglobals.focuser.connect()
        self.focuser_settings()

    def focuser_settings(self):
        self.focuser_position_spinbox.setMaximum(appglobals.focuser.max_step())
        self.focuser_position_spinbox.blockSignals(True)
        self.focuser_position_spinbox.setValue(appglobals.focuser.position())
        self.focuser_position_spinbox.blockSignals(False)
        if appglobals.focuser.temp_comp_available():
            if appglobals.focuser.is_temp_comp():
                self.temp_checkbox.setChecked(True)
            else:
                self.temp_checkbox.setChecked(False)
            self.temp_checkbox.setVisible(True)
        else:
            self.temp_checkbox.setVisible(False)
        if not appglobals.focuser.absolute():
            messagebox = QtWidgets.QMessageBox()
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setText("ASCOM Focusers without Absolute Focusing are not supported!")
            messagebox.exec_()
            self.focuser_action.setChecked(False)

    def move_focuser(self):
        if appglobals.focuser.absolute():
            position = self.focuser_position_spinbox.text()
            appglobals.focuser.move(position)

        # TODO: Implement relative focusing
        else:
            old_pos = appglobals.focuser.position()
            position = int(self.focuser_position_spinbox.text()) - old_pos
            print("\nself.focuser_position_spinbox.text() =", int(self.focuser_position_spinbox.text()),
                  "\nold_pos =", old_pos, "\nposition =", position)
            appglobals.focuser.move(position)

    def temp_comp(self):
        state = self.temp_checkbox.isChecked()
        if state:
            self.focuser_position_label.setEnabled(False)
            self.focuser_position_spinbox.setEnabled(False)
        else:
            self.focuser_position_label.setEnabled(True)
            self.focuser_position_spinbox.setEnabled(True)
        appglobals.focuser.temp_comp(state)

    def connect_filters(self):
        if self.wheel_group.isChecked():
            name = "The filter wheel"
            try:
                appglobals.wheel = ascom.FilterWheel()
                name = appglobals.wheel.name_()
                self.wheel_name_label.setText(name)
            except Exception as e:
                print(e)
                self.wheel_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.wheel_group.isChecked():
            try:
                self.temp_checkbox.setVisible(False)
                self.temp_checkbox.setChecked(False)
                appglobals.wheel.disconnect()
                appglobals.wheel.dispose()
            except AttributeError as e:
                print(e)
            finally:
                appglobals.wheel = None
                self.wheel_name_label.setText("Not Connected")

    @staticmethod
    def setup_filterwheel():
        appglobals.wheel.disconnect()
        appglobals.wheel.setup_dialog()
        appglobals.wheel.connect()
        # self.filterwheel_settings()

    def change_filter(self):
        try:
            text = self.position_combobox.currentText()
            appglobals.wheel.rotate_wheel(text)
        except AttributeError as e:
            print(e)

    def showEvent(self, event: QtGui.QShowEvent):
        """Override default showEvent method."""
        self.setVisible(True)
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.setVisible(True)
