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
import numpy
import appglobals
import connectcamera
import zwosettings
import guiderparameters
from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QTableWidgetItem
from astropy.time import Time
from astropy.coordinates import get_body
from ui.ui_mainwindow import Ui_MainWindow
from ui.delegates import QDateEditItemDelegate, QTimeEditItemDelegate, QComboBoxItemDelegate, QSpinBoxItemDelegate
from thread import CameraThread
from equipment import zwo

if sys.platform.startswith("win"):
    from equipment import ascom


EXPOSURE_UNIT = "ms"
GAIN_UNIT = "e/adu"
INTEGRATION_UNIT = "s"
CUTOFF_UNIT = "nm"


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.telescope = None
        self.camera = None
        self.guider = None
        self.wheel = None
        self.focuser = None

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
        self.date_delegate = QDateEditItemDelegate(self)
        self.time_delegate = QTimeEditItemDelegate(self)
        self.target_delegate = QComboBoxItemDelegate(self, self.target_list_model)
        # TODO: Create delegate for parameters column.

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
            lambda: self.telescope.move_axis(1, self.mount_trackrate_spin.cleanText())
        )
        self.slewnorth_button.pressed.connect(
            lambda: self.telescope.move_axis(1, self.mount_trackrate_spin.cleanText())
        )
        self.sleweast_button.pressed.connect(
            lambda: self.telescope.move_axis(0, self.mount_trackrate_spin.cleanText())
        )
        self.slewsouth_button.pressed.connect(
            lambda: self.telescope.move_axis(1, -1 * float(self.mount_trackrate_spin.cleanText()))
        )
        self.slewwest_button.pressed.connect(
            lambda: self.telescope.move_axis(0, -1 * float(self.mount_trackrate_spin.cleanText()))
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
        self.slewnorth_button.released.connect(lambda: self.telescope.move_axis(1, 0.0))
        self.sleweast_button.released.connect(lambda: self.telescope.move_axis(0, 0.0))
        self.slewsouth_button.released.connect(lambda: self.telescope.move_axis(1, 0.0))
        self.slewwest_button.released.connect(lambda: self.telescope.move_axis(0, 0.0))
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

        self.load_filters(appglobals.filters)

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
        self.schedule_table.setItemDelegateForColumn(0, self.date_delegate)
        self.schedule_table.setItemDelegateForColumn(1, self.time_delegate)
        self.schedule_table.setItemDelegateForColumn(2, self.target_delegate)
        # TODO: Set delegate for parameters column.

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
                    value = item.text()
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
                self.telescope = ascom.AscomTelescope()
                self.telescope_settings()
                name = self.telescope.name
                self.telescope_name_label.setText(name)
            except Exception as e:
                print(e)
                self.mount_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.mount_group.isChecked():
            try:
                self.telescope.connected = False
                self.telescope.dispose()
            except AttributeError as e:
                print(e)
            self.telescope = None
            self.telescope_name_label.setText("Not Connected")

    def setup_telescope(self):
        self.telescope.connected = False
        self.telescope.setup_dialog()
        self.telescope.connected = True
        self.telescope_settings()

    def telescope_settings(self):
        if not self.telescope.can_slew_eq:
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
            self.telescope.goto_home()
        elif self.object_combobox.currentText() == "Stop" or self.sender() is self.slewstop_button:
            self.telescope.tracking = False
        else:
            body = get_body(self.object_combobox.currentText().lower(), Time.now())
            self.telescope.goto(body.ra.hour, body.dec.degree)

    def slew_diagonal(self, rate1: float, rate2: float):
        self.telescope.move_axis(0, rate1)
        self.telescope.move_axis(1, rate2)

    def connect_guider(self):
        if self.guider_group.isChecked():
            guider_dialog = connectcamera.ConnectCamera()
            guider_dialog.exec_()
            name = "The guider"
            try:
                if not guider_dialog.asi_selected and guider_dialog.accepted:
                    self.guider = ascom.AscomCamera()
                    name = self.guider.name
                    self.guider_name_label.setText(name)
                    self.guider_menu.addAction(self.ascomguidersettings_action)
                elif guider_dialog.asi_selected and guider_dialog.accepted:
                    self.guider = zwo.ZwoCamera(asi.list_cameras().index(guider_dialog.asi_camera))
                    self.guider_settings_frame.set_camera(self.guider)
                    self.guider_name_label.setText(guider_dialog.asi_camera)
                    self.guider_menu.addAction(self.guider_settings_action)
                else:
                    raise Exception
                self.setup_guider_controls()
            except Exception as e:
                print(e)
                self.guider_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.guider_group.isChecked():
            try:
                if type(self.guider) is ascom.AscomCamera:
                    self.guider_menu.removeAction(self.ascomguidersettings_action)
                    self.guider.connected = False
                    self.guider.dispose()
                elif type(self.guider) is zwo.ZwoCamera:
                    self.guider_menu.removeAction(self.guider_settings_action)
                    self.guider.close()
            except AttributeError as e:
                print(e)
            finally:
                self.guider = None
                self.guider_settings_frame.set_camera(self.guider)
                self.guider_name_label.setText("Not Connected")

    def setup_guider(self):
        self.guider.connected = False
        self.guider.setup_dialog()
        self.guider.connected = True
        self.setup_guider_controls()

    def set_guider_exposure(self):
        self.guider.exposure = int(self.guider_exposure_spinbox.cleanText())

    def set_guider_gain(self):
        self.guider.gain = int(self.guider_gain_spinbox.cleanText())

    def setup_guider_controls(self):
        if self.guider.has_gain:
            self.guider_gain_spinbox.setMinimum(self.guider.min_gain)
            self.guider_gain_spinbox.setMaximum(self.guider.max_gain)
            self.guider_gain_slider.setMinimum(self.guider.min_gain)
            self.guider_gain_slider.setMaximum(self.guider.max_gain)
            self.guider_gain_spinbox.setValue(self.guider.gain)
        else:
            self.guider_gain_label.setEnabled(False)
            self.guider_gain_spinbox.setEnabled(False)
            self.guider_gain_slider.setEnabled(False)

        if self.guider.has_exposure:
            self.guider_exposure_spinbox.setMinimum(self.guider.min_exposure)
            self.guider_exposure_spinbox.setMaximum(self.guider.max_exposure)
            self.guider_exposure_slider.setMinimum(self.guider.min_exposure)
            self.guider_exposure_slider.setMaximum(self.guider.max_exposure)
            self.guider_exposure_spinbox.setValue(self.guider.exposure)
        else:
            self.guider_exposure_label.setEnabled(False)
            self.guider_exposure_spinbox.setEnabled(False)
            self.guider_exposure_slider.setEnabled(False)

        if self.guider is zwo.ZwoCamera:
            self.guider_settings_frame.setup_controls(self.guider)

    def guider_loop(self):
        if self.guider_loop_button.isChecked():
            if self.guider_start_button.isChecked():
                self.guider_thread = threading.Thread(target=self.guider_preview)  # To be implemented
            else:
                self.guider_thread = CameraThread(self.guider, self.guider_loop_button)
                self.guider_thread.exposure_done.connect(self.guider_preview)
            self.guider_thread.daemon = True
            self.guider_thread.start()

    def guider_preview(self, frame: numpy.ndarray):
        image = Image.fromarray(frame)
        pix = ImageQt.toqpixmap(image)
        self.guider_preview_label.setPixmap(pix)

    def connect_camera(self):
        if self.camera_group.isChecked():
            name = "The camera"
            camera_dialog = connectcamera.ConnectCamera()
            camera_dialog.exec_()
            try:
                if not camera_dialog.asi_selected and camera_dialog.accepted:
                    self.camera = ascom.AscomCamera()
                    name = self.camera.name
                    self.camera_name_label.setText(name)
                    self.camera_settings_menu.insertAction(self.savelocation_action, self.ascomcamerasettings_action)
                elif camera_dialog.asi_selected and camera_dialog.accepted:
                    self.camera = zwo.ZwoCamera(asi.list_cameras().index(camera_dialog.asi_camera))
                    self.camera_settings_frame.set_camera(self.camera)
                    self.camera_name_label.setText(camera_dialog.asi_camera)
                    self.camera_settings_action.setDefaultWidget(self.camera_settings_frame)
                    self.camera_settings_menu.insertAction(self.savelocation_action, self.camera_settings_action)
                else:
                    raise Exception
                self.setup_camera_controls()
            except Exception as e:
                print(e)
                self.camera_group.setChecked(False)
                self.connect_fail_dialog(name)

        elif not self.camera_group.isChecked():
            try:
                if type(self.camera) is ascom.AscomCamera:
                    self.camera_settings_menu.removeAction(self.ascomcamerasettings_action)
                    self.camera.connected = False
                    self.camera.dispose()
                elif type(self.camera) is zwo.ZwoCamera:
                    self.camera_settings_menu.removeAction(self.camera_settings_action)
                    self.camera.connected = False
            except AttributeError as e:
                print(e)
            finally:
                self.camera = None
                self.camera_settings_frame.set_camera(self.camera)
                self.camera_name_label.setText("Not Connected")

    def setup_camera_controls(self):
        # TODO: Test these statements with more cameras that support different features
        if self.camera.has_gain:
            self.camera_gain_spinbox.setMinimum(self.camera.min_gain)
            self.camera_gain_spinbox.setMaximum(self.camera.max_gain)
            self.camera_gain_slider.setMinimum(self.camera.min_gain)
            self.camera_gain_slider.setMaximum(self.camera.max_gain)
            self.camera_gain_spinbox.setValue(self.camera.gain)
        else:
            self.camera_gain_label.setEnabled(False)
            self.camera_gain_spinbox.setEnabled(False)
            self.camera_gain_slider.setEnabled(False)

        if self.camera.has_exposure:
            self.camera_exposure_spinbox.setMinimum(self.camera.min_exposure)
            self.camera_exposure_spinbox.setMaximum(self.camera.max_exposure)
            self.camera_exposure_slider.setMinimum(self.camera.min_exposure)
            self.camera_exposure_slider.setMaximum(self.camera.max_exposure)
            self.camera_exposure_spinbox.setValue(self.camera.exposure)
        else:
            self.camera_exposure_label.setEnabled(False)
            self.camera_exposure_spinbox.setEnabled(False)
            self.camera_exposure_slider.setEnabled(False)

        if self.camera is zwo.ZwoCamera:
            self.camera_settings_frame.setup_controls(self.camera)

    def setup_camera(self):
        self.camera.connected = False
        self.camera.setup_dialog()
        self.camera.connected = True
        self.setup_camera_controls()

    def set_camera_exposure(self):
        self.camera.exposure = int(self.camera_exposure_spinbox.cleanText())

    def set_camera_gain(self):
        self.camera.gain = int(self.camera_gain_spinbox.cleanText())

    def camera_loop(self):
        if self.camera_loop_button.isChecked():
            if self.camera_capture_button.isChecked():
                self.camera_thread = threading.Thread(target=self.camera_record)
            else:
                self.camera_thread = CameraThread(self.camera, self.camera_loop_button)
                self.camera_thread.exposure_done.connect(self.camera_preview)
            self.camera_thread.daemon = True
            self.camera_thread.start()

    def camera_preview(self, pixmap: QtGui.QPixmap):
        self.camera_preview_label.setPixmap(pixmap)

    def camera_record(self):
        name_format = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        avi_name = "{}/{}.avi".format(appglobals.settings["Save Directory"], name_format)
        out = cv2.VideoWriter(avi_name, 0, 0, tuple(self.camera.roi_resolution), False)
        while self.camera_capture_button.isChecked():
            image = self.camera.get_frame()
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
        camera_dir_dialog = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            appglobals.settings["Save Directory"],
            QtWidgets.QFileDialog.DontUseNativeDialog
        )

        if str(camera_dir_dialog) == "":
            pass
        else:
            appglobals.settings["Save Directory"] = str(camera_dir_dialog)
            self.save_settings()

    def connect_focuser(self):
        if self.focuser_group.isChecked():
            name = "The focuser"
            try:
                self.focuser = ascom.AscomFocuser()
                self.focuser_settings()
                name = self.focuser.name
                self.focuser_name_label.setText(name)
            except Exception as e:
                print(e)
                self.focuser_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.focuser_group.isChecked():
            try:
                self.temp_checkbox.setVisible(False)
                self.temp_checkbox.setChecked(False)
                self.focuser.connected = False
                self.focuser.dispose()
            except AttributeError as e:
                print(e)
            finally:
                self.focuser = None
                self.focuser_name_label.setText("Not Connected")

    def setup_focuser(self):
        self.focuser.connected = False
        self.focuser.setup_dialog()
        self.focuser.connected = True
        self.focuser_settings()

    def focuser_settings(self):
        self.focuser_position_spinbox.setMaximum(self.focuser.max_step)
        self.focuser_position_spinbox.blockSignals(True)
        self.focuser_position_spinbox.setValue(self.focuser.position)
        self.focuser_position_spinbox.blockSignals(False)
        if self.focuser.has_temp_comp():
            if self.focuser.temp_comp:
                self.temp_checkbox.setChecked(True)
            else:
                self.temp_checkbox.setChecked(False)
            self.temp_checkbox.setVisible(True)
        else:
            self.temp_checkbox.setVisible(False)
        if not self.focuser.is_abs_position():
            messagebox = QtWidgets.QMessageBox()
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setText("ASCOM Focusers without Absolute Focusing are not supported!")
            messagebox.exec_()
            self.focuser_action.setChecked(False)

    def move_focuser(self):
        if self.focuser.is_abs_position():
            position = self.focuser_position_spinbox.text()
            self.focuser.position = position

        # TODO: Implement relative focusing
        else:
            old_pos = self.focuser.position
            position = int(self.focuser_position_spinbox.text()) - old_pos
            print("\nself.focuser_position_spinbox.text() =", int(self.focuser_position_spinbox.text()),
                  "\nold_pos =", old_pos, "\nposition =", position)
            self.focuser.position = position

    def temp_comp(self):
        state = self.temp_checkbox.isChecked()
        if state:
            self.focuser_position_label.setEnabled(False)
            self.focuser_position_spinbox.setEnabled(False)
        else:
            self.focuser_position_label.setEnabled(True)
            self.focuser_position_spinbox.setEnabled(True)
        self.focuser.temp_comp = state

    def connect_filters(self):
        if self.wheel_group.isChecked():
            name = "The filter wheel"
            try:
                self.wheel = ascom.AscomFilterWheel()
                name = self.wheel.name
                self.wheel_name_label.setText(name)
            except Exception as e:
                print(e)
                self.wheel_group.setChecked(False)
                self.connect_fail_dialog(name)
        elif not self.wheel_group.isChecked():
            try:
                self.temp_checkbox.setVisible(False)
                self.temp_checkbox.setChecked(False)
                self.wheel.connected = False
                self.wheel.dispose()
            except AttributeError as e:
                print(e)
            finally:
                self.wheel = None
                self.wheel_name_label.setText("Not Connected")

    def setup_filterwheel(self):
        self.wheel.connected = False
        self.wheel.setup_dialog()
        self.wheel.connected = True
        # self.filterwheel_settings()

    def change_filter(self):
        try:
            text = self.position_combobox.currentText()
            self.wheel.rotate_wheel(text)
        except AttributeError as e:
            print(e)

    def showEvent(self, event: QtGui.QShowEvent):
        """Override default showEvent method."""
        self.setVisible(True)
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.setVisible(True)
