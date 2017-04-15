import os
import sys
import json
import threading
import ephem
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageQt
from ui_mainwindow import Ui_MainWindow
import res_rc
import modifylocation
import targetswindow
from computetargets import ComputeTargets
import appglobals
if sys.platform.startswith('win'):
    import ascomequipment


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.menu = QtWidgets.QMenu()
        self.tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(':/icons/logo.svg'))
        self.was_hidden = False
        self.status_coords_label = QtWidgets.QLabel()
        self.setupUi(self)

        self.row_count = self.schedule_table.rowCount()

        self.mountmodes_tuple = ("Stop", "Home")

        if os.path.exists("filters.json"):
            with open("filters.json", "r") as f:
                try:
                    self.filters = json.load(f)
                except json.decoder.JSONDecodeError:
                    self.filters = {}
        else:
            self.filters = {}

        if os.path.exists("schedule.json"):
            with open("schedule.json", "r") as f:
                try:
                    self.schedule = json.load(f)
                except json.decoder.JSONDecodeError:
                    self.schedule = {}
        else:
            self.schedule = {}

        self.t = []

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
        self.tabifyDockWidget(self.schedule_dockwidget, self.autoguide_dockwidget)
        self.tabifyDockWidget(self.autoguide_dockwidget, self.camera_dockwidget)
        self.tabifyDockWidget(self.camera_dockwidget, self.filters_dockwidget)
        self.schedule_dockwidget.raise_()
        self.camera_dockwidget.setVisible(False)
        self.autoguide_dockwidget.setVisible(False)

        self.slewstop_button.clicked.connect(self.goto_target)
        self.telescope_action.toggled.connect(self.connect_telescope)
        self.camera_action.toggled.connect(self.connect_camera)
        self.guide_action.toggled.connect(self.connect_autoguider)
        self.focuser_action.toggled.connect(self.connect_focuser)
        self.wheel_action.toggled.connect(self.connect_filters)

        self.scope_settings_btn.clicked.connect(self.setup_telescope)
        self.camera_settings_btn.clicked.connect(self.setup_camera)
        self.guide_settings_btn.clicked.connect(self.setup_autoguider)
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

        self.guider_loop_button.clicked.connect(self.autoguider_loop)
        self.camera_loop_button.clicked.connect(self.camera_loop)

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
            'Latitude: ' + str(appglobals.location["Latitude"]) + '°,  Longitude: ' +
            str(appglobals.location["Longitude"]) + "°")
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
        for f in self.filters:
            self.position_combobox.addItem(f.get("Name"))
            self.camera_filter_combobox.addItem(f["Name"])

        self.position_combobox.lineEdit().returnPressed.connect(self.change_filter)
        self.position_combobox.currentIndexChanged.connect(self.change_filter)

        self.temp_checkbox.setVisible(False)

        self.addrow_button_2.clicked.connect(self.add_filter_row)
        self.removerow_button_2.clicked.connect(self.remove_filter_row)

        date = self.schedule_dateedit.text()
        self.load_schedule(date)
        self.load_filters(self.filters)

        self.schedule_dateedit.dateChanged.connect(lambda: self.load_schedule(
            str(self.schedule_dateedit.text())))

        self.schedule_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.filter_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

    # Add row in schedule_table
    def add_schedule_row(self):
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
        for f in self.filters:
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

        self.save_schedule()

    # Remove selected rows from schedule_table
    def remove_schedule_row(self):
        index_list = []
        date = self.schedule_dateedit.text()
        for model_index in self.schedule_table.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.schedule_table.removeRow(index.row())
            del self.schedule[date][index.row()]
        self.save_schedule()

    # Save contents of schedule_table into schedule.json
    def save_schedule(self):
        if os.path.exists('schedule.json'):
            os.remove('schedule.json')
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
            self.schedule.update({self.schedule_dateedit.text(): schedule_list})
        with open('schedule.json', 'a') as f:
            json.dump(self.schedule, f, indent=4)

    # Load contents of schedule.json into schedule_table
    def load_schedule(self, schedule):
        count = 0
        self.schedule_table.setRowCount(0)
        try:
            for f in self.schedule[schedule]:
                self.add_schedule_row()
                time = QtCore.QTime.fromString(f['Time'])
                target = self.schedule_table.cellWidget(count, 1).findText(f['Target'], QtCore.Qt.MatchFixedString)
                set_filter = self.schedule_table.cellWidget(count, 2).findText(f['Filter'], QtCore.Qt.MatchFixedString)

                self.schedule_table.cellWidget(count, 0).blockSignals(True)
                self.schedule_table.cellWidget(count, 1).blockSignals(True)
                self.schedule_table.cellWidget(count, 2).blockSignals(True)
                self.schedule_table.cellWidget(count, 3).blockSignals(True)
                self.schedule_table.cellWidget(count, 4).blockSignals(True)
                self.schedule_table.cellWidget(count, 5).blockSignals(True)

                self.schedule_table.cellWidget(count, 0).setTime(time)
                self.schedule_table.cellWidget(count, 1).setCurrentIndex(target)
                self.schedule_table.cellWidget(count, 2).setCurrentIndex(set_filter)
                self.schedule_table.cellWidget(count, 3).setValue(int(f['Exposure']))
                self.schedule_table.cellWidget(count, 4).setValue(int(f['Gain']))
                self.schedule_table.cellWidget(count, 5).setValue(int(f['Integration']))

                self.schedule_table.cellWidget(count, 0).blockSignals(False)
                self.schedule_table.cellWidget(count, 1).blockSignals(False)
                self.schedule_table.cellWidget(count, 2).blockSignals(False)
                self.schedule_table.cellWidget(count, 3).blockSignals(False)
                self.schedule_table.cellWidget(count, 4).blockSignals(False)
                self.schedule_table.cellWidget(count, 5).blockSignals(False)

        except KeyError:
            pass
        count += 1

    # Add row in filter_table
    def add_filter_row(self):
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

        lower_spinbox.setSuffix('nm')
        upper_spinbox.setSuffix('nm')

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

    # Remove selected rows from filter_table
    def remove_filter_row(self):
        index_list = []
        for model_index in self.filter_table.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.filter_table.removeRow(index.row())

    # Save contents of filter_table into filters.json
    def save_filters(self):
        if os.path.exists('filters.json'):
            os.remove('filters.json')
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
        with open('filters.json', 'a') as f:
            json.dump(filter_list, f, indent=0)
        with open("filters.json", "r") as f:
            self.filters = json.load(f)
        for row in range(self.schedule_table.rowCount()):
            text = self.schedule_table.cellWidget(row, 2).currentText()
            cbox = self.schedule_table.cellWidget(row, 2)
            cbox.clear()
            for f in self.filters:
                cbox.addItem(f["Name"])
            index = cbox.findText(text)
            cbox.setCurrentIndex(index)
        self.position_combobox.blockSignals(True)
        text = self.position_combobox.currentText()
        text2 = self.camera_filter_combobox.currentText()
        self.position_combobox.clear()
        self.camera_filter_combobox.clear()
        self.camera_filter_combobox.addItem("None")
        for f in self.filters:
            self.camera_filter_combobox.addItem(f["Name"])
            self.position_combobox.addItem(f["Name"])
        index = self.position_combobox.findText(text)
        self.position_combobox.setCurrentIndex(index)
        self.position_combobox.blockSignals(False)
        index = self.position_combobox.findText(text2)
        self.position_combobox.setCurrentIndex(index)

    # Load contents of filters.json into filter_table
    def load_filters(self, filters):
        count = 0
        for f in filters:
            self.add_filter_row()
            self.filter_table.cellWidget(count, 0).setText(f['Name'])
            self.filter_table.cellWidget(count, 1).setText(f['Brand'])
            self.filter_table.cellWidget(count, 2).setValue(int(f['Wheel Position']))
            self.filter_table.cellWidget(count, 3).setValue(int(f['Lower Cutoff']))
            self.filter_table.cellWidget(count, 4).setValue(int(f['Upper Cutoff']))
            count += 1

    # Set observing location
    def location_set(self):
        location_dialog = modifylocation.LocationDialog()
        location_dialog.exec_()
        if os.path.exists("location.json"):
            with open("location.json", "r") as f:
                appglobals.location = json.load(f)
        self.status_coords_label.setText(
            'Latitude: ' + str(appglobals.location["Latitude"]) + u"°,  Longitude: " + str(
                appglobals.location["Longitude"]) + u"°")
        self.target_dialog.generate(appglobals.location["Latitude"], appglobals.location["Longitude"])

    # Show window with chart of planet elevations throughout the day
    def open_target_gui(self):
        self.target_dialog.show()

    # Notify users if connection to equipment fails
    def connect_fail_dialog(self, name):
        messagebox = QtWidgets.QMessageBox()
        messagebox.setIcon(QtWidgets.QMessageBox.Warning)
        messagebox.setWindowTitle("Solar System Sequencer")
        messagebox.setText("{0} failed to connect.".format(name))
        messagebox.exec_()

    # <editor-fold desc="Telescope">

    def connect_telescope(self):
        if self.mount_group.isChecked():
            name = "The telescope"
            try:
                appglobals.telescope = ascomequipment.Telescope()
                self.telescope_settings()
                name = appglobals.telescope.name_()
                self.telescope_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Telescope Connected", "{0} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.mount_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{0} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
        elif not self.mount_group.isChecked():
            try:
                appglobals.telescope.disconnect()
                appglobals.telescope.dispose()
            except AttributeError:
                pass
            appglobals.telescope = None
            self.telescope_name_label.setText('Not Connected')

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

    def compute_target(self, target, time, print_=False):
        if target == 'Stop' or target == 'Home' or target == '':
            self.goto_target()
        else:
            compute_alt = ComputeTargets(time, appglobals.location["Latitude"], appglobals.location["Longitude"])
            alt = compute_alt.object_alt(target)
            if print_:
                print("Target: %-5s, Time: %-19s, RA: %-11s, Dec°: %-11s, Az: %-11s, Alt°: %-11s"
                      % (target, str(time), str(ephem.hours(alt["ra"])), str(ephem.degrees(alt["dec"])),
                         str(ephem.degrees(alt["az"])), str(ephem.degrees(alt["alt"]))))
            return alt

    def goto_target(self):
        goto_thread = threading.Thread(target=self.goto_target_thread)
        goto_thread.start()

    def goto_target_thread(self):
        if self.object_combobox.currentText() == 'Home':
            appglobals.telescope.home()
        elif self.object_combobox.currentText() == 'Stop' or self.sender() is self.slewstop_button:
            appglobals.telescope.stop_tracking()
        else:
            coords = self.compute_target(self.object_combobox.currentText(), ephem.now())
            ra_split = str(ephem.hours(coords["ra"]))
            ra_split = ra_split.split(":")
            ra_decimal = int(ra_split[0]) + (int(ra_split[1]) / 60) + (float(ra_split[2]) / 3600)
            dec_split = str(ephem.degrees(coords["dec"]))
            dec_split = dec_split.split(":")

            if int(dec_split[0]) >= 0:
                dec_decimal = int(dec_split[0]) + (int(dec_split[1]) / 60) + (float(dec_split[2]) / 3600)
            else:
                dec_decimal = int(dec_split[0]) + ((-1 * int(dec_split[1])) / 60) + (-1 * float(dec_split[2]) / 3600)
            appglobals.telescope.goto(ra_decimal, dec_decimal)

    def slew(self, axis, rate):
        appglobals.telescope.move_axis(axis, rate)

    def slew_diagonal(self, rate1, rate2):
        appglobals.telescope.move_axis(0, rate1)
        appglobals.telescope.move_axis(1, rate2)

    # </editor-fold>

    # <editor-fold desc="Auto-guider">

    def connect_autoguider(self):
        if self.autoguide_group.isChecked():
            name = "The auto-guider"
            try:
                appglobals.guider = ascomequipment.Camera()
                self.autoguider_settings()
                name = appglobals.guider.name_()
                self.guide_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Auto-Guider Connected", "{0} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.autoguide_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{0} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
        elif not self.autoguide_group.isChecked():
            try:
                appglobals.guider.disconnect()
                appglobals.guider.dispose()
            except AttributeError as e:
                pass
            appglobals.guider = None
            self.guide_name_label.setText('Not Connected')

    def setup_autoguider(self):
        appglobals.guider.disconnect()
        appglobals.guider.setup_dialog()
        appglobals.guider.connect()
        self.autoguider_settings()

    def autoguider_settings(self):
        self.guider_gain_spinbox.setMinimum(appglobals.guider.gain_min())
        self.guider_gain_spinbox.setMaximum(appglobals.guider.gain_max())
        self.guider_gain_slider.setMinimum(appglobals.guider.gain_min())
        self.guider_gain_slider.setMaximum(appglobals.guider.gain_max())
        self.guider_gain_spinbox.setValue(appglobals.guider.gain())
        self.guider_exposure_spinbox.setMinimum(appglobals.guider.exposure_min() * 1000)
        self.guider_exposure_spinbox.setMaximum(appglobals.guider.exposure_max() * 1000)
        self.guider_exposure_slider.setMinimum(appglobals.guider.exposure_min() * 1000)
        self.guider_exposure_slider.setMaximum(appglobals.guider.exposure_max() * 1000)

    def autoguider_loop(self):
        thread = threading.Thread(target=self.autoguider_loop_thread)
        thread.daemon = True
        thread.start()

    def autoguider_loop_thread(self):
        while self.guider_loop_button.isChecked():
            exp_sec = float(self.guider_exposure_spinbox.cleanText()) / 1000
            image = appglobals.guider.capture(exp_sec, True)
            pix = ImageQt.toqpixmap(image)
            self.guide_preview_label.setPixmap(pix)

    # </editor-fold>

    # <editor-fold desc="Imaging Camera">

    def connect_camera(self):
        if self.camera_group.isChecked():
            name = "The camera"
            try:
                appglobals.camera = ascomequipment.Camera()
                self.camera_settings()
                name = appglobals.camera.name_()
                self.camera_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Camera Connected", "{0} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.camera_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{0} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
        elif not self.camera_group.isChecked():
            try:
                appglobals.camera.disconnect()
                appglobals.camera.dispose()
            except AttributeError:
                pass
            appglobals.camera = None
            self.camera_name_label.setText('Not Connected')

    def setup_camera(self):
        appglobals.camera.disconnect()
        appglobals.camera.setup_dialog()
        appglobals.camera.connect()
        self.camera_settings()

    def camera_settings(self):
        self.camera_gain_spinbox.setMinimum(appglobals.camera.gain_min())
        self.camera_gain_spinbox.setMaximum(appglobals.camera.gain_max())
        self.camera_gain_slider.setMinimum(appglobals.camera.gain_min())
        self.camera_gain_slider.setMaximum(appglobals.camera.gain_max())
        self.camera_gain_spinbox.setValue(appglobals.camera.gain())
        self.camera_exposure_spinbox.setMinimum(appglobals.camera.exposure_min() * 1000)
        self.camera_exposure_spinbox.setMaximum(appglobals.camera.exposure_max() * 1000)
        self.camera_exposure_slider.setMinimum(appglobals.camera.exposure_min() * 1000)
        self.camera_exposure_slider.setMaximum(appglobals.camera.exposure_max() * 1000)

    def camera_loop(self):
        if self.camera_loop_button.isChecked():
            thread = threading.Thread(target=self.camera_loop_thread)
            thread.daemon = True
            thread.start()
        else:
            self.camera_capture_button.setChecked(False)

    def camera_loop_thread(self):
        avi_name = '{}.avi'.format(str(ephem.now()).replace('/', '-').replace(':', '', 1).replace(':', '_'))
        out = cv2.VideoWriter(avi_name, -1, 20.0, (appglobals.camera.num_x(), appglobals.camera.num_y()), False)
        while self.camera_loop_button.isChecked():
            exp_sec = float(self.camera_exposure_spinbox.cleanText()) / 1000
            image = appglobals.camera.capture(exp_sec, True)
            if self.camera_capture_button.isChecked():
                out.write(image)
            image = Image.fromarray(image)
            pix = ImageQt.toqpixmap(image)
            self.camera_preview_label.setPixmap(pix)
        out.release()
        if os.path.getsize(avi_name) == 0:
            os.remove(avi_name)

    # </editor-fold>

    # <editor-fold desc="Focuser">

    def connect_focuser(self):
        if self.focuser_group.isChecked():
            name = "The focuser"
            try:
                appglobals.focuser = ascomequipment.Focuser()
                self.focuser_settings()
                name = appglobals.focuser.name_()
                self.focuser_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Focuser Connected", "{0} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.focuser_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{0} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
        elif not self.focuser_group.isChecked():
            try:
                self.temp_checkbox.setVisible(False)
                self.temp_checkbox.setChecked(False)
                appglobals.focuser.disconnect()
                appglobals.focuser.dispose()
            except AttributeError as e:
                print(e)
            appglobals.focuser = None
            self.focuser_name_label.setText('Not Connected')

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
        if appglobals.focuser.absolute:
            position = self.focuser_position_spinbox.text()
            appglobals.focuser.move(position)
        ''' Attempt at Relative Focusing
        old_pos = app_globals.devices["Focuser"].focuser_position()
        else:
            position = int(self.focuser_position_spinbox.text()) - old_pos
            print(int(self.focuser_position_spinbox.text()), old_pos, position)
        '''

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
                appglobals.wheel = ascomequipment.FilterWheel()
                name = appglobals.wheel.name_()
                self.wheel_name_label.setText(name)
                if self.isHidden():
                    self.tray_icon.showMessage("Filter Wheel Connected", "{0} has been connected.".format(name),
                                               QtWidgets.QSystemTrayIcon.Information)
            except Exception as e:
                print(e)
                self.wheel_group.setChecked(False)
                if self.isVisible():
                    self.connect_fail_dialog(name)
                else:
                    self.tray_icon.showMessage("Connection Failed", "{0} failed to connect.".format(name),
                                               QtWidgets.QSystemTrayIcon.Warning)
        elif not self.wheel_group.isChecked():
            try:
                self.temp_checkbox.setVisible(False)
                self.temp_checkbox.setChecked(False)
                appglobals.wheel.disconnect()
                appglobals.wheel.dispose()
            except AttributeError as e:
                print(e)
            appglobals.wheel = None
            self.wheel_name_label.setText('Not Connected')

    def setup_filterwheel(self):
        appglobals.wheel.disconnect()
        appglobals.wheel.setup_dialog()
        appglobals.wheel.connect()
        #self.filterwheel_settings()

    def change_filter(self):
        try:
            text = self.position_combobox.currentText()
            appglobals.wheel.rotate_wheel(text)
        except AttributeError:
            pass

    # </editor-fold>

    def close_app(self):
        appglobals.telescope = None
        appglobals.camera = None
        appglobals.guider = None
        appglobals.focuser = None
        appglobals.wheel = None
        sys.exit()

    # Override default closeEvent method
    def closeEvent(self, event):
        event.ignore()
        self.setVisible(False)
        self.target_dialog.setVisible(False)
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.setVisible(False)

    # Override default showEvent method
    def showEvent(self, event):
        self.setVisible(True)
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.setVisible(True)
