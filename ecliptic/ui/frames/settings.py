import os
import sys
import json
from PySide6 import QtWidgets
from .uic.uic_settings import Ui_SettingsFrame
from ui.frames.filters import FiltersFrame
from thread import TelescopeConnectThread
from connectcamera import ConnectCamera
import appglobals
from equipment import zwo
from astrometry.astap import AstapSolver
import zwosettings

if sys.platform.startswith("win"):
    from equipment import ascom


class SettingsFrame(QtWidgets.QFrame, Ui_SettingsFrame):
    def __init__(self, parent):
        self.parent = parent
        
        super().__init__(self.parent)
        self.setupUi(self)
        
        self.telescope_check_box.toggled.connect(self.parent.telescope_action.setChecked)
        self.guider_check_box.toggled.connect(self.parent.guider_action.setChecked)
        self.camera_check_box.toggled.connect(self.parent.camera_action.setChecked)
        self.filter_wheel_check_box.toggled.connect(self.parent.wheel_action.setChecked)
        self.focuser_check_box.toggled.connect(self.parent.focuser_action.setChecked)

        self.telescope_check_box.toggled.connect(self.connect_telescope)
        self.guider_check_box.toggled.connect(self.connect_guider)
        self.camera_check_box.toggled.connect(self.connect_camera)
        self.filter_wheel_check_box.toggled.connect(self.connect_filters)
        self.focuser_check_box.toggled.connect(self.connect_focuser)

        self.telescope_settings_button.clicked.connect(self.setup_telescope)
        self.guider_settings_button.clicked.connect(self.setup_guider)
        self.camera_settings_button.clicked.connect(self.setup_camera)
        self.filter_wheel_settings_button.clicked.connect(self.setup_filterwheel)
        self.focuser_settings_button.clicked.connect(self.setup_focuser)

        # Insert filter settings.
        self.filters_layout = QtWidgets.QVBoxLayout(self.filters_group_box)
        self.filters_layout.addWidget(FiltersFrame(self))
        self.filters_group_box.setLayout(self.filters_layout)
        
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

        self.astap_location_button.clicked.connect(self.set_astap_dir)
        if "ASTAP Location" in appglobals.settings.keys():
            self.astap_location_line_edit.setText(appglobals.settings['ASTAP Location'])
    
    def connect_telescope(self, b):
        if self.telescope_check_box.isChecked():
            name = "The telescope"
            self.setup_thread = TelescopeConnectThread(self.parent.telescope, self)
            self.setup_thread.setup_complete.connect(self.telescope_settings)
            self.setup_thread.setup_complete.connect(self.parent.can_plate_solve)
            self.setup_thread.setup_failed.connect(self.telescope_connect_failed)
            self.setup_thread.daemon = True
            self.setup_thread.start()
        elif not self.telescope_check_box.isChecked():
            try:
                self.parent.telescope.connected = False
                self.parent.telescope.dispose()
            except AttributeError as e:
                print(e)
            finally:
                self.parent.telescope = None
                self.parent.can_plate_solve()
                self.telescope_check_box.setText("Telescope")
                self.parent.mount_group.setEnabled(False)
    
    def telescope_settings(self, telescope):
        self.parent.telescope = telescope
        name = self.parent.telescope.name
        self.telescope_check_box.setText(f'Telescope ({name})')
        self.parent.mount_group.setEnabled(True)
        if not self.parent.telescope.can_slew_eq:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setText("ASCOM Telescopes that can't accept equatorial coordinates are not supported!")
            messagebox.exec_()
            self.parent.telescope_action.setChecked(False)
    
    def setup_telescope(self):
        self.parent.telescope.connected = False
        self.parent.telescope.setup_dialog()
        self.parent.telescope.connected = True
        self.telescope_settings(self.parent.telescope)
    
    def telescope_connect_failed(self, e: Exception):
        print(e)
        self.telescope_check_box.setChecked(False)
        self.parent.connect_fail_dialog("Telescope")
    
    def connect_guider(self):
        if self.guider_check_box.isChecked():
            name = "The guider"
            guider_dialog = ConnectCamera()
            guider_dialog.exec_()
            try:
                self.parent.guider = guider_dialog.result
                if type(self.parent.guider) is ascom.AscomCamera:
                    name = self.parent.guider.name
                    self.guider_check_box.setText(f'Guider ({name})')
                    self.parent.guider_menu.addAction(self.parent.ascomguidersettings_action)
                elif type(self.parent.guider) is zwo.ZwoCamera:
                    self.parent.guider_settings_frame.set_camera(self.parent.guider)
                    self.guider_check_box.setText(f'Guider ({self.parent.guider.name})')
                    self.parent.guider_menu.addAction(self.parent.guider_settings_action)
                else:
                    raise Exception
                self.parent.guider_group.setEnabled(True)
                self.parent.setup_guider_controls()
            except Exception as e:
                print(e)
                self.parent.guider_group.setEnabled(False)
                self.guider_check_box.setChecked(False)
                self.parent.connect_fail_dialog(name)
        elif not self.guider_check_box.isChecked():
            try:
                if type(self.parent.guider) is ascom.AscomCamera:
                    self.parent.guider_menu.removeAction(self.ascomguidersettings_action)
                    self.parent.guider.connected = False
                    self.parent.guider.dispose()
                elif type(self.parent.guider) is zwo.ZwoCamera:
                    self.parent.guider_menu.removeAction(self.parent.guider_settings_action)
                    self.parent.guider.close()
            except AttributeError as e:
                print(e)
            finally:
                self.parent.guider = None
                self.parent.guider_settings_frame.set_camera(self.parent.guider)
                self.guider_check_box.setText("Guider")
                self.parent.guider_group.setEnabled(False)
        self.parent.can_plate_solve()

    def setup_guider(self):
        self.parent.guider.connected = False
        self.parent.guider.setup_dialog()
        self.parent.guider.connected = True
        self.parent.setup_guider_controls()

    def connect_camera(self):
        if self.camera_check_box.isChecked():
            name = "The camera"
            camera_dialog = ConnectCamera()
            camera_dialog.exec_()
            try:
                self.parent.camera = camera_dialog.result
                if type(self.parent.camera) is ascom.AscomCamera:
                    name = self.parent.camera.name
                    self.camera_check_box.setText(f'Camera ({name})')
                    self.parent.camera_settings_menu.insertAction(self.parent.savelocation_action, self.parent.ascomcamerasettings_action)
                elif type(self.parent.camera) is zwo.ZwoCamera:
                    self.parent.camera_settings_frame.set_camera(self.parent.camera)
                    self.camera_check_box.setText(f'Camera ({self.parent.camera.name})')
                    self.parent.camera_settings_action.setDefaultWidget(self.parent.camera_settings_frame)
                    self.parent.camera_settings_menu.insertAction(self.parent.savelocation_action, self.parent.camera_settings_action)
                else:
                    raise Exception
                self.parent.camera_group.setEnabled(True)
                self.parent.setup_camera_controls()
            except Exception as e:
                print(e)
                self.camera_check_box.setChecked(False)
                self.parent.camera_group.setEnabled(False)
                self.parent.connect_fail_dialog(name)

        elif not self.camera_check_box.isChecked():
            try:
                if type(self.parent.camera) is ascom.AscomCamera:
                    self.parent.camera_settings_menu.removeAction(self.parent.ascomcamerasettings_action)
                    self.parent.camera.connected = False
                    self.parent.camera.dispose()
                elif type(self.parent.camera) is zwo.ZwoCamera:
                    self.parent.camera_settings_menu.removeAction(self.parent.camera_settings_action)
                    self.parent.camera.connected = False
            except AttributeError as e:
                print(e)
            finally:
                self.parent.camera = None
                self.parent.camera_settings_frame.set_camera(self.parent.camera)
                self.camera_check_box.setText("Camera")
                self.parent.camera_group.setEnabled(False)
    
    def setup_camera(self):
        self.parent.camera.connected = False
        self.parent.camera.setup_dialog()
        self.parent.camera.connected = True
        self.parent.setup_camera_controls()
    
    def connect_filters(self):
        if self.filter_wheel_check_box.isChecked():
            name = "The filter wheel"
            try:
                self.parent.wheel = ascom.AscomFilterWheel()
                name = self.parent.wheel.name
                self.filter_wheel_check_box.setText(f'Filter Wheel ({name})')
                self.parent.wheel_group.setEnabled(True)
            except Exception as e:
                print(e)
                self.filter_wheel_check_box.setChecked(False)
                self.parent.wheel_group.setDisabled(True)
                self.parent.connect_fail_dialog(name)
        elif not self.filter_wheel_check_box.isChecked():
            try:
                self.parent.temp_checkbox.setVisible(False)
                self.parent.temp_checkbox.setChecked(False)
                self.parent.wheel.connected = False
                self.parent.wheel.dispose()
            except AttributeError as e:
                print(e)
            finally:
                self.parent.wheel = None
                self.filter_wheel_check_box.setText("Filter wheel")
                self.parent.wheel_group.setDisabled(True)
    
    def setup_filterwheel(self):
        self.parent.wheel.connected = False
        self.parent.wheel.setup_dialog()
        self.parent.wheel.connected = True
        # self.parent.filterwheel_settings()
    
    def connect_focuser(self):
        if self.focuser_check_box.isChecked():
            name = "The focuser"
            try:
                self.parent.focuser = ascom.AscomFocuser()
                self.parent.focuser_settings()
                name = self.parent.focuser.name
                self.focuser_check_box.setText(f'Focuser ({name})')
                self.parent.focuser_group.setEnabled(True)
            except Exception as e:
                print(e)
                self.focuser_check_box.setChecked(False)
                self.parent.focuser_group.setDisabled(True)
                self.parent.connect_fail_dialog(name)
        elif not self.focuser_check_box.isChecked():
            try:
                self.parent.temp_checkbox.setVisible(False)
                self.parent.temp_checkbox.setChecked(False)
                self.parent.focuser.connected = False
                self.parent.focuser.dispose()
            except AttributeError as e:
                print(e)
            finally:
                self.parent.focuser = None
                self.focuser_check_box.setText('Focuser')
                self.parent.focuser_group.setDisabled(True)

    def setup_focuser(self):
        self.parent.focuser.connected = False
        self.parent.focuser.setup_dialog()
        self.parent.focuser.connected = True
        self.parent.focuser_settings()

        if self.parent.focuser.has_temp_comp():
            if self.parent.focuser.temp_comp:
                self.parent.temp_checkbox.setChecked(True)
            else:
                self.parent.temp_checkbox.setChecked(False)
            self.parent.temp_checkbox.setVisible(True)
        else:
            self.parent.temp_checkbox.setVisible(False)
        if not self.parent.focuser.is_abs_position():
            messagebox = QtWidgets.QMessageBox()
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setText("ASCOM Focusers without Absolute Focusing are not supported!")
            messagebox.exec_()
            self.focuser_action.setChecked(False)
    
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
        self.parent.status_coords_label.setText(
            "Latitude: %d°%d\'%d\", Longitude: %d°%d\'%d\"" % (
                appglobals.location["Latitude"][0],
                appglobals.location["Latitude"][1],
                appglobals.location["Latitude"][2],
                appglobals.location["Longitude"][0],
                appglobals.location["Longitude"][1],
                appglobals.location["Longitude"][2]
            )
        )

    def set_astap_dir(self):
        if "ASTAP Location" in appglobals.settings.keys():
            default_dir = appglobals.settings["ASTAP Location"]
        else:
            default_dir = None
        
        astap_dialog = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select ASTAP executable",
            default_dir,
            filter="Executable files (*.exe);;All files (*.*)",
            options = QtWidgets.QFileDialog.DontUseNativeDialog
        )

        if str(astap_dialog[0]) != "":
            appglobals.settings["ASTAP Location"] = str(astap_dialog[0])
            self.parent.save_settings()
            self.astap_location_line_edit.setText(str(astap_dialog[0]))
            self.parent.guider_frame.set_solver(AstapSolver(self.astap_location_line_edit.text()))
