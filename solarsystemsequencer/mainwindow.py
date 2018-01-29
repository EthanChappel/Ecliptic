import json
import os
import sys
import threading
from datetime import datetime
from typing import List, Dict
import cv2
import ephem
import zwoasi as asi
from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets
import appglobals
import connectcamera
import modifylocation
import targetswindow
import zwosettings
import guiderparameters
import computetargets
from ui.ui_mainwindow import Ui_MainWindow

if sys.platform.startswith("win"):
    from equipment import ascom


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.firstclose = True
        self.camera_thread = None
        self.guider_thread = None

        self.menu = QtWidgets.QMenu()
        self.tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(":/icons/logo.svg"))
        self.was_hidden = False
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

        if sys.platform.startswith("win"):
            asi.init(str(sys.path[0]) + "\\lib\\ASICamera2.dll")

        self.target_dialog = targetswindow.TargetsDialog()

        self.setup_gui()

    def setup_gui(self):
        # Center window on screen
        window_size = self.frameGeometry()
        desktop = QtWidgets.QDesktopWidget().availableGeometry().center()
        window_size.moveCenter(desktop)
        self.move(window_size.topLeft())

        # Tray icon
        self.menu.addAction(self.exit_action)
        show_action = self.menu.addAction("Open")
        self.menu.addMenu(self.menu_equipment)
        show_action.triggered.connect(self.show)
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        self.tabifyDockWidget(self.schedule_dockwidget, self.guider_dockwidget)
        self.tabifyDockWidget(self.guider_dockwidget, self.camera_dockwidget)
        self.tabifyDockWidget(self.camera_dockwidget, self.filters_dockwidget)
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
        self.slewnorth_button.pressed.connect(lambda: self.slew(1, self.mount_trackrate_spin.cleanText()))
        self.slewnorth_button.pressed.connect(lambda: self.slew(1, self.mount_trackrate_spin.cleanText()))
        self.sleweast_button.pressed.connect(lambda: self.slew(0, self.mount_trackrate_spin.cleanText()))
        self.slewsouth_button.pressed.connect(
            lambda: self.slew(1, -1 * float(self.mount_trackrate_spin.cleanText())))
        self.slewwest_button.pressed.connect(
            lambda: self.slew(0, -1 * float(self.mount_trackrate_spin.cleanText())))
        self.slewnortheast_button.pressed.connect(
            lambda: self.slew_diagonal(self.mount_trackrate_spin.cleanText(),
                                       self.mount_trackrate_spin.cleanText()))
        self.slewsoutheast_button.pressed.connect(
            lambda: self.slew_diagonal(self.mount_trackrate_spin.cleanText(),
                                       -1 * float(self.mount_trackrate_spin.cleanText())))
        self.slewsouthwest_button.pressed.connect(
            lambda: self.slew_diagonal(-1 * float(self.mount_trackrate_spin.cleanText()),
                                       -1 * float(self.mount_trackrate_spin.cleanText())))
        self.slewnorthwest_button.pressed.connect(
            lambda: self.slew_diagonal(-1 * float(self.mount_trackrate_spin.cleanText()),
                                       self.mount_trackrate_spin.cleanText()))

        # Connects clicked event that stops mount to the directional buttons
        self.slewnorth_button.released.connect(lambda: self.slew(1, 0.0))
        self.sleweast_button.released.connect(lambda: self.slew(0, 0.0))
        self.slewsouth_button.released.connect(lambda: self.slew(1, 0.0))
        self.slewwest_button.released.connect(lambda: self.slew(0, 0.0))
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
        self.location_action.triggered.connect(self.location_set)
        self.targets_action.triggered.connect(self.open_target_gui)
        self.exit_action.triggered.connect(self.close_app)

        # Add targets to object_combobox
        self.object_combobox.addItems(self.mountmodes_tuple)
        self.object_combobox.addItems(appglobals.targets_tuple)

        # Set label to show latitude and longitude and show it on status bar
        self.status_coords_label.setText(
            "Latitude: " + str(appglobals.location["Latitude"][0]) + "°" +
            str(appglobals.location["Latitude"][1]) + "\'" +
            str(appglobals.location["Latitude"][2]) + "\"" +
            ",  Longitude: " + str(appglobals.location["Longitude"][0]) + "°" +
            str(appglobals.location["Longitude"][1]) + "\'" +
            str(appglobals.location["Longitude"][2]) + "\"")
        self.statusbar.addWidget(self.status_coords_label)

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

    def add_schedule_row(self):
        """Add row in schedule_table."""
        self.row_count = self.schedule_table.rowCount()
        self.schedule_table.insertRow(self.row_count)

        # Create QTimeEdit for Time Column
        time_timeedit = QtWidgets.QTimeEdit()
        time_timeedit.setDisplayFormat("HH:mm:ss")

        # Create QComboBox for Target Column
        target_combobox = QtWidgets.QComboBox()
        target_combobox.addItems(self.mountmodes_tuple)
        target_combobox.addItems(appglobals.targets_tuple)
        target_combobox.setCurrentIndex(-1)

        # Create QComboBox for Filter Column
        filter_combobox = QtWidgets.QComboBox()
        for f in appglobals.filters:
            filter_combobox.addItem(f.get("Name"))
        filter_combobox.setCurrentIndex(-1)

        # Create QSpinBox for Exposure Column
        exposure_spinbox = QtWidgets.QSpinBox()
        exposure_spinbox.setSuffix("ms")

        # Create QSpinBox for Gain Column
        gain_spinbox = QtWidgets.QSpinBox()
        gain_spinbox.setSuffix("e/adu")

        # Create QSpinBox for Integration Column
        integration_spinbox = QtWidgets.QSpinBox()
        integration_spinbox.setSuffix("s")

        time_timeedit.editingFinished.connect(self.save_schedule)
        target_combobox.currentIndexChanged.connect(self.save_schedule)
        filter_combobox.currentIndexChanged.connect(self.save_schedule)
        exposure_spinbox.editingFinished.connect(self.save_schedule)
        gain_spinbox.editingFinished.connect(self.save_schedule)
        integration_spinbox.editingFinished.connect(self.save_schedule)

        # Add widgets to their cells in schedule_table
        self.schedule_table.setCellWidget(self.row_count, 0, time_timeedit)
        self.schedule_table.setCellWidget(self.row_count, 1, target_combobox)
        self.schedule_table.setCellWidget(self.row_count, 2, filter_combobox)
        self.schedule_table.setCellWidget(self.row_count, 3, exposure_spinbox)
        self.schedule_table.setCellWidget(self.row_count, 4, gain_spinbox)
        self.schedule_table.setCellWidget(self.row_count, 5, integration_spinbox)

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
                try:
                    value = str(self.schedule_table.cellWidget(row, col).currentText())
                except AttributeError:
                    try:
                        value = str(self.schedule_table.cellWidget(row, col).cleanText())
                    except AttributeError:
                        value = str(self.schedule_table.cellWidget(row, col).text())
                schedule_dict.update({header: value})
            schedule_list.append(schedule_dict)
            appglobals.schedule.update({self.schedule_dateedit.text(): schedule_list})
        print(sys._getframe(1).f_code.co_name)
        with open("schedule.json", "w") as f:
            json.dump(appglobals.schedule, f, indent=4)

    def load_schedule(self, date: str):
        """Load contents of schedule.json into schedule_table."""
        self.schedule_table.setRowCount(0)
        if date in appglobals.schedule:
            count = 0
            for f in appglobals.schedule[date]:
                self.add_schedule_row()

                self.schedule_table.cellWidget(count, 0).blockSignals(True)
                self.schedule_table.cellWidget(count, 1).blockSignals(True)
                self.schedule_table.cellWidget(count, 2).blockSignals(True)
                self.schedule_table.cellWidget(count, 3).blockSignals(True)
                self.schedule_table.cellWidget(count, 4).blockSignals(True)
                self.schedule_table.cellWidget(count, 5).blockSignals(True)

                time = QtCore.QTime.fromString(f["Time"])
                target = self.schedule_table.cellWidget(count, 1).findText(f["Target"], QtCore.Qt.MatchFixedString)
                set_filter = self.schedule_table.cellWidget(count, 2).findText(f["Filter"], QtCore.Qt.MatchFixedString)

                print(time.toString(), target, set_filter, int(f["Exposure"]), int(f["Gain"]), int(f["Integration"]))

                self.schedule_table.cellWidget(count, 0).setTime(time)
                self.schedule_table.cellWidget(count, 1).setCurrentIndex(target)
                self.schedule_table.cellWidget(count, 2).setCurrentIndex(set_filter)
                self.schedule_table.cellWidget(count, 3).setValue(int(f["Exposure"]))
                self.schedule_table.cellWidget(count, 4).setValue(int(f["Gain"]))
                self.schedule_table.cellWidget(count, 5).setValue(int(f["Integration"]))

                self.schedule_table.cellWidget(count, 0).blockSignals(False)
                self.schedule_table.cellWidget(count, 1).blockSignals(False)
                self.schedule_table.cellWidget(count, 2).blockSignals(False)
                self.schedule_table.cellWidget(count, 3).blockSignals(False)
                self.schedule_table.cellWidget(count, 4).blockSignals(False)
                self.schedule_table.cellWidget(count, 5).blockSignals(False)
                count += 1

    def add_filter_row(self):
        """Add row in filter_table."""
        self.row_count = self.filter_table.rowCount()
        self.filter_table.insertRow(self.row_count)

        name_lineedit = QtWidgets.QLineEdit()
        pos_spinbox = QtWidgets.QSpinBox()
        lower_spinbox = QtWidgets.QSpinBox()
        upper_spinbox = QtWidgets.QSpinBox()
        brand_lineedit = QtWidgets.QLineEdit()

        name_lineedit.editingFinished.connect(self.save_filters)
        pos_spinbox.editingFinished.connect(self.save_filters)
        lower_spinbox.editingFinished.connect(self.save_filters)
        upper_spinbox.editingFinished.connect(self.save_filters)
        brand_lineedit.editingFinished.connect(self.save_filters)

        lower_spinbox.setSuffix("nm")
        upper_spinbox.setSuffix("nm")

        pos_spinbox.setMinimum(0)
        lower_spinbox.setMinimum(0)
        upper_spinbox.setMinimum(0)

        lower_spinbox.setMaximum(1999)
        upper_spinbox.setMaximum(2000)

        self.filter_table.setCellWidget(self.row_count, 0, name_lineedit)
        self.filter_table.setCellWidget(self.row_count, 1, brand_lineedit)
        self.filter_table.setCellWidget(self.row_count, 2, pos_spinbox)
        self.filter_table.setCellWidget(self.row_count, 3, lower_spinbox)
        self.filter_table.setCellWidget(self.row_count, 4, upper_spinbox)

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
                try:
                    value = str(self.filter_table.cellWidget(row, col).cleanText())
                except AttributeError:
                    value = str(self.filter_table.cellWidget(row, col).text())
                filter_dict.update({header: value})
            filter_list.append(filter_dict)
        with open("filters.json", "a") as f:
            json.dump(filter_list, f, indent=0)
        with open("filters.json", "r") as f:
            appglobals.filters = json.load(f)
        for row in range(self.schedule_table.rowCount()):
            cbox = self.schedule_table.cellWidget(row, 2)
            text = cbox.currentText()
            cbox.blockSignals(True)
            cbox.clear()
            for f in appglobals.filters:
                cbox.addItem(f["Name"])
            index = cbox.findText(text)
            cbox.blockSignals(False)
            cbox.setCurrentIndex(index)
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

            self.filter_table.cellWidget(count, 0).blockSignals(True)
            self.filter_table.cellWidget(count, 1).blockSignals(True)
            self.filter_table.cellWidget(count, 2).blockSignals(True)
            self.filter_table.cellWidget(count, 3).blockSignals(True)
            self.filter_table.cellWidget(count, 4).blockSignals(True)

            self.filter_table.cellWidget(count, 0).setText(f["Name"])
            self.filter_table.cellWidget(count, 1).setText(f["Brand"])
            self.filter_table.cellWidget(count, 2).setValue(int(f["Wheel Position"]))
            self.filter_table.cellWidget(count, 3).setValue(int(f["Lower Cutoff"]))
            self.filter_table.cellWidget(count, 4).setValue(int(f["Upper Cutoff"]))

            self.filter_table.cellWidget(count, 0).blockSignals(False)
            self.filter_table.cellWidget(count, 1).blockSignals(False)
            self.filter_table.cellWidget(count, 2).blockSignals(False)
            self.filter_table.cellWidget(count, 3).blockSignals(False)
            self.filter_table.cellWidget(count, 4).blockSignals(False)
            count += 1

    def location_set(self):
        """Set observing location."""
        location_dialog = modifylocation.LocationDialog()
        location_dialog.exec_()
        if os.path.exists("location.json"):
            with open("location.json", "r") as f:
                appglobals.location = json.load(f)
        self.status_coords_label.setText(
            "Latitude: " + str(appglobals.location["Latitude"][0]) + "°" +
            str(appglobals.location["Latitude"][1]) + "\'" +
            str(appglobals.location["Latitude"][2]) + "\"" +
            ",  Longitude: " + str(appglobals.location["Longitude"][0]) + "°" +
            str(appglobals.location["Longitude"][1]) + "\'" +
            str(appglobals.location["Longitude"][2]) + "\"")
        self.target_dialog.generate()

    def open_target_gui(self):
        """Show window with chart of planet elevations throughout the day."""
        self.target_dialog.show()

    @staticmethod
    def connect_fail_dialog(name: str):
        """Notify users if connection to equipment fails."""
        messagebox = QtWidgets.QMessageBox()
        messagebox.setIcon(QtWidgets.QMessageBox.Warning)
        messagebox.setWindowTitle("Solar System Sequencer - Connection Failed")
        messagebox.setText("{} failed to connect.".format(name))
        messagebox.exec_()

    # <editor-fold desc="Telescope">

    def connect_telescope(self):
        if self.mount_group.isChecked():
            name = "The telescope"
            try:
                appglobals.telescope = ascom.Telescope()
                self.telescope_settings()
                name = appglobals.telescope.name_()
                self.telescope_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Telescope Connected", "{} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.mount_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
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
        if not appglobals.telescope.canslew_eq():
            messagebox = QtWidgets.QMessageBox()
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setText("ASCOM Telescopes that can't accept equatorial coordinates are not supported!")
            messagebox.exec_()
            self.telescope_action.setChecked(False)

    @staticmethod
    def compute_ra(target: str, time: datetime, print_: bool=False):
        ra = computetargets.get_ra(target, time, appglobals.location["Latitude"], appglobals.location["Longitude"])
        if print_:
            print("Target: %-5s, Time: %-19s, RA: %-11s" % (target, str(time), str(ephem.hours(ra))))
        return ra

    @staticmethod
    def compute_dec(target: str, time: datetime, print_: bool=False):
        dec = computetargets.get_dec(target, time, appglobals.location["Latitude"], appglobals.location["Longitude"])
        if print_:
            print("Target: %-5s, Time: %-19s, Dec°: %-11s" % (target, str(time), str(ephem.degrees(dec))))
        return dec

    def goto_target(self):
        goto_thread = threading.Thread(target=self.goto_target_thread)
        goto_thread.start()

    def goto_target_thread(self):
        if self.object_combobox.currentText() == "Home":
            appglobals.telescope.home()
        elif self.object_combobox.currentText() == "Stop" or self.sender() is self.slewstop_button:
            appglobals.telescope.stop_tracking()
        else:
            ra = self.compute_ra(self.object_combobox.currentText(), ephem.now().datetime())
            dec = self.compute_dec(self.object_combobox.currentText(), ephem.now().datetime())
            ra_split = str(ephem.hours(ra))
            ra_split = ra_split.split(":")
            ra_decimal = int(ra_split[0]) + (int(ra_split[1]) / 60) + (float(ra_split[2]) / 3600)
            dec_split = str(ephem.degrees(dec))
            dec_split = dec_split.split(":")

            if int(dec_split[0]) >= 0:
                dec_decimal = int(dec_split[0]) + (int(dec_split[1]) / 60) + (float(dec_split[2]) / 3600)
            else:
                dec_decimal = int(dec_split[0]) + ((-1 * int(dec_split[1])) / 60) + (-1 * float(dec_split[2]) / 3600)
            appglobals.telescope.goto(ra_decimal, dec_decimal)

    @staticmethod
    def slew(axis: int, rate: float):
        appglobals.telescope.move_axis(axis, rate)

    @staticmethod
    def slew_diagonal(rate1: float, rate2: float):
        appglobals.telescope.move_axis(0, rate1)
        appglobals.telescope.move_axis(1, rate2)

    # </editor-fold>

    # <editor-fold desc="Guider">

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
                    if self.isHidden():
                        self.tray_icon.showMessage("Guider Connected", "{} has been connected.".format(name),
                                                   QtWidgets.QSystemTrayIcon.Information)
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
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
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

    # </editor-fold>

    # <editor-fold desc="Camera">

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
                    if self.isHidden():
                        self.tray_icon.showMessage("Camera Connected", "{} has been connected.".format(name),
                                                   QtWidgets.QSystemTrayIcon.Information)
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
                if self.isVisible() and camera_dialog.accepted:
                    self.connect_fail_dialog(name)
                elif self.isHidden() and camera_dialog.accepted:
                    self.tray_icon.showMessage("Connection Failed", "{} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)

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
        name_format = str(ephem.now()).replace("/", "-").replace(":", "", 1).replace(":", "_")
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

    # </editor-fold>

    # <editor-fold desc="Focuser">

    def connect_focuser(self):
        if self.focuser_group.isChecked():
            name = "The focuser"
            try:
                appglobals.focuser = ascom.Focuser()
                self.focuser_settings()
                name = appglobals.focuser.name_()
                self.focuser_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Focuser Connected", "{} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.focuser_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
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

    # </editor-fold>

    # <editor-fold desc="Filter Wheel">

    def connect_filters(self):
        if self.wheel_group.isChecked():
            name = "The filter wheel"
            try:
                appglobals.wheel = ascom.FilterWheel()
                name = appglobals.wheel.name_()
                self.wheel_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Filter Wheel Connected", "{} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.wheel_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
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

    # </editor-fold>

    def close_app(self):
        self.mount_group.setChecked(False)
        self.guider_group.setChecked(False)
        self.camera_group.setChecked(False)
        self.focuser_group.setChecked(False)
        self.wheel_group.setChecked(False)
        sys.exit()

    def closeEvent(self, event: QtGui.QCloseEvent):
        """Override default closeEvent method."""
        event.ignore()
        self.setVisible(False)
        self.target_dialog.setVisible(False)
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.setVisible(False)
        if self.firstclose:
            self.firstclose = False
            self.tray_icon.showMessage("Running in background", "Solar System Sequencer is still running in the "
                                                                "background.", QtWidgets.QSystemTrayIcon.Information)

    def showEvent(self, event: QtGui.QShowEvent):
        """Override default showEvent method."""
        self.setVisible(True)
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.setVisible(True)
