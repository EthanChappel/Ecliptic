import json
import os
import sys
import threading
from datetime import datetime
from formats.ser3 import Ser3Writer
import zwoasi as asi
from PIL import Image, ImageQt
from PySide6 import QtCore, QtGui, QtWidgets
import appglobals
from ui.windows.zwosettings import ZWOSettings
from ui.windows.guiderparameters import GuiderParameters
from ui.windows.uic.uic_mainwindow import Ui_MainWindow
from ui.frames.schedule import ScheduleFrame
from ui.frames.guider import GuiderFrame
from ui.frames.camera import CameraFrame
from ui.frames.settings import SettingsFrame
from ui.widgets.dockwindow import DockWindow
from thread import TelescopeSlewThread, CameraThread, FinderCameraThread
from equipment import zwo

if sys.platform.startswith("win"):
    from equipment import ascom


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    start_recording = QtCore.Signal(Ser3Writer)
    stop_recording = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.telescope = None
        self.camera = None
        self.guider = None
        self.wheel = None
        self.focuser = None

        self.telescope_thread = None
        self.camera_thread = None
        self.guider_thread = None

        self.menu = QtWidgets.QMenu()
        self.status_coords_label = QtWidgets.QLabel()
        self.setupUi(self)

        self.camera_settings_frame = ZWOSettings()
        self.camera_settings_action = QtWidgets.QWidgetAction(None)
        self.camera_settings_menu = QtWidgets.QMenu()
        self.camera_settings_menu.addAction(self.savelocation_action)
        self.camera_settings_btn.setMenu(self.camera_settings_menu)

        self.guider_settings_frame = ZWOSettings()
        self.guider_parameters_frame = GuiderParameters()
        self.guider_settings_action = QtWidgets.QWidgetAction(None)
        self.guider_settings_action.setDefaultWidget(self.guider_settings_frame)
        self.guider_parameters_action = QtWidgets.QWidgetAction(None)
        self.guider_parameters_action.setDefaultWidget(self.guider_parameters_frame)
        self.guider_menu = QtWidgets.QMenu()
        self.guider_menu.addAction(self.guider_parameters_action)
        self.guider_settings_btn.setMenu(self.guider_menu)

        self.mountmodes_tuple = ("Stop", "Home")

        # Models for schedule table columns.
        self.target_list_model = QtCore.QStringListModel()
        self.target_list_model.setStringList(self.mountmodes_tuple + appglobals.targets_tuple)

        # Schedule frame
        self.schedule_dockwindow = DockWindow(self, windowTitle='Schedule')
        self.schedule_dockwindow.setFeatures(self.schedule_dockwindow.features() & ~QtWidgets.QDockWidget.DockWidgetClosable)
        self.schedule_frame = ScheduleFrame(self)
        self.schedule_dockwindow.setWidget(self.schedule_frame)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.schedule_dockwindow)
        
        # Guider frame
        self.guider_dockwindow = DockWindow(self, windowTitle='Guider')
        self.guider_dockwindow.setFeatures(self.guider_dockwindow.features() & ~QtWidgets.QDockWidget.DockWidgetClosable)
        self.guider_frame = GuiderFrame(self)
        self.guider_dockwindow.setWidget(self.guider_frame)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.guider_dockwindow)

        # Camera frame
        self.camera_dockwindow = DockWindow(self, windowTitle='Camera')
        self.camera_dockwindow.setFeatures(self.camera_dockwindow.features() & ~QtWidgets.QDockWidget.DockWidgetClosable)
        self.camera_frame = CameraFrame(self)
        self.camera_dockwindow.setWidget(self.camera_frame)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.camera_dockwindow)

        # Settings frame
        self.settings_dockwindow = DockWindow(self, windowTitle='Settings')
        self.settings_frame = SettingsFrame(self)
        self.settings_dockwindow.setWidget(self.settings_frame)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.settings_dockwindow)
        
        self.telescope_action.toggled.connect(self.settings_frame.telescope_check_box.setChecked)
        self.guider_action.toggled.connect(self.settings_frame.guider_check_box.setChecked)
        self.camera_action.toggled.connect(self.settings_frame.camera_check_box.setChecked)
        self.wheel_action.toggled.connect(self.settings_frame.filter_wheel_check_box.setChecked)
        self.focuser_action.toggled.connect(self.settings_frame.focuser_check_box.setChecked)

        if sys.platform.startswith("win"):
            asi.init(str(sys.path[0]) + "\\lib\\ASICamera2.dll")

        self.setup_gui()

    def setup_gui(self):
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        self.tabifyDockWidget(self.schedule_dockwindow, self.guider_dockwindow)
        self.tabifyDockWidget(self.guider_dockwindow, self.camera_dockwindow)
        self.tabifyDockWidget(self.camera_dockwindow, self.settings_dockwindow)
        self.schedule_dockwindow.raise_()
        self.camera_dockwindow.setVisible(False)
        self.guider_dockwindow.setVisible(False)

        self.ascomcamerasettings_action.triggered.connect(self.settings_frame.setup_camera)
        self.ascomguidersettings_action.triggered.connect(self.settings_frame.setup_guider)

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

        self.guider_snap_button.clicked.connect(self.guider_snap)
        self.camera_loop_button.clicked.connect(self.camera_loop)
        self.camera_capture_button.toggled.connect(self.camera_record)

        # Connect functions to actions
        self.location_action.triggered.connect(lambda: self.settings_dockwindow.raise_())

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

        self.focuser_position_spinbox.setKeyboardTracking(False)
        self.focuser_position_spinbox.lineEdit().returnPressed.connect(self.move_focuser)
        self.focuser_position_spinbox.valueChanged.connect(self.move_focuser)
        self.temp_checkbox.stateChanged.connect(self.temp_comp)

        # Add targets to position_combobox
        self.position_combobox.addItem("None")
        for f in appglobals.filters:
            self.position_combobox.addItem(f.get("Name"))

        self.position_combobox.lineEdit().returnPressed.connect(self.change_filter)
        self.position_combobox.currentIndexChanged.connect(self.change_filter)

        self.temp_checkbox.setVisible(False)

        self.camera_exposure_spinbox.valueChanged.connect(self.set_camera_exposure)
        self.camera_exposure_slider.valueChanged.connect(self.set_camera_exposure)
        self.camera_gain_spinbox.valueChanged.connect(self.set_camera_gain)
        self.camera_gain_slider.valueChanged.connect(self.set_camera_gain)

        self.guider_exposure_spinbox.valueChanged.connect(self.set_guider_exposure)
        self.guider_exposure_slider.valueChanged.connect(self.set_guider_exposure)
        self.guider_gain_spinbox.valueChanged.connect(self.set_guider_gain)
        self.guider_gain_slider.valueChanged.connect(self.set_guider_gain)

        self.savelocation_action.triggered.connect(self.change_camera_save_dir)

    @staticmethod
    def connect_fail_dialog(name: str):
        """Notify users if connection to equipment fails."""
        messagebox = QtWidgets.QMessageBox()
        messagebox.setIcon(QtWidgets.QMessageBox.Warning)
        messagebox.setWindowTitle("Ecliptic - Connection Failed")
        messagebox.setText("{} failed to connect.".format(name))
        messagebox.exec_()

    def goto_target(self, verify=False):
        self.telescope_thread = TelescopeSlewThread(self.telescope, self.object_combobox.currentText())
        self.telescope_thread.daemon = True
        self.telescope_thread.start()

    def slew_diagonal(self, rate1: float, rate2: float):
        self.telescope.move_axis(0, rate1)
        self.telescope.move_axis(1, rate2)

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

        if type(self.guider) is zwo.ZwoCamera:
            self.guider_settings_frame.setup_controls(self.guider)

    def guider_snap(self):
        self.guider_thread = FinderCameraThread(self.guider, None, self)
        self.guider_thread.exposure_done.connect(self.guider_frame.preview)
        self.guider_thread.exposure_done.connect(self.can_plate_solve)
        self.guider_thread.daemon = True
        self.guider_thread.start()

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

        if type(self.camera) is zwo.ZwoCamera:
            self.camera_settings_frame.setup_controls(self.camera)

    def set_camera_exposure(self):
        self.camera.exposure = int(self.camera_exposure_spinbox.cleanText())

    def set_camera_gain(self):
        self.camera.gain = int(self.camera_gain_spinbox.cleanText())

    def camera_loop(self):
        if self.camera_loop_button.isChecked():
            self.camera_thread = CameraThread(self.camera, self.camera_loop_button, self)
            self.camera_thread.exposure_done.connect(self.camera_frame.preview)
            self.camera_thread.daemon = True
            self.camera_thread.start()

    def camera_record(self):
        if self.camera_capture_button.isChecked():
            name_format = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            avi_name = "{}/{}.ser".format(appglobals.settings["Save Directory"], name_format)
            roi = self.camera.roi_resolution
            camera_name = self.settings_frame.observer_camera_combo_box.currentText()
            observer_name = self.settings_frame.observer_name_combo_box.currentText()
            telescope_name = self.settings_frame.observer_telescope_combo_box.currentText()
            writer = Ser3Writer(avi_name, 0, True, roi[0], roi[1], 8, observer_name, camera_name, telescope_name)
            self.start_recording.emit(writer)
        else:
            self.stop_recording.emit()

    def save_settings(self):
        """Save application settings into settings.json."""
        if os.path.exists("settings.json"):
            os.remove("settings.json")

        with open("settings.json", "a") as f:
            json.dump(appglobals.settings, f, indent=4)

    def change_camera_save_dir(self):
        if "Save Directory" in appglobals.settings.keys():
            default_dir = appglobals.settings["Save Directory"]
        else:
            default_dir = None
        
        camera_dir_dialog = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            default_dir,
            QtWidgets.QFileDialog.DontUseNativeDialog
        )

        if str(camera_dir_dialog) == "":
            pass
        else:
            appglobals.settings["Save Directory"] = str(camera_dir_dialog)
            self.save_settings()

    def focuser_settings(self):
        self.focuser_position_spinbox.setMaximum(self.focuser.max_step)
        self.focuser_position_spinbox.blockSignals(True)
        self.focuser_position_spinbox.setValue(self.focuser.position)
        self.focuser_position_spinbox.blockSignals(False)

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

    def change_filter(self):
        try:
            text = self.position_combobox.currentText()
            self.wheel.rotate_wheel(text)
        except AttributeError as e:
            print(e)
    
    @QtCore.Slot()
    def update_filters(self):
        self.position_combobox.blockSignals(True)
        text = self.position_combobox.currentText()
        self.position_combobox.clear()
        self.position_combobox.addItem("None")
        for f in appglobals.filters:
            self.position_combobox.addItem(f["Name"])
        index = self.position_combobox.findText(text)
        self.position_combobox.setCurrentIndex(index)
        self.position_combobox.blockSignals(False)
        index = self.position_combobox.findText(text2)
        self.position_combobox.setCurrentIndex(index)
    
    @QtCore.Slot()
    def can_plate_solve(self):
        can_solve = bool(self.telescope and self.guider and self.guider_frame.image)
        self.guider_frame.plate_solve_button.setEnabled(can_solve)
        return can_solve

    def showEvent(self, event: QtGui.QShowEvent):
        """Override default showEvent method."""
        self.setVisible(True)
        for dock in self.findChildren(QtWidgets.QDockWidget):
            dock.setVisible(True)
