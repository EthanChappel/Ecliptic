import os
import json
from PySide6 import QtWidgets
from .uic.uic_settings import Ui_SettingsFrame
from ui.frames.filters import FiltersFrame
from thread import TelescopeThread
import appglobals


class SettingsFrame(QtWidgets.QFrame, Ui_SettingsFrame):
    def __init__(self, parent):
        self.parent = parent
        
        super().__init__(self.parent)
        self.setupUi(self)

        
        self.telescope_check_box.toggled.connect(self.parent.telescope_action.setChecked)

        self.telescope_check_box.toggled.connect(self.connect_telescope)
        self.telescope_settings_button.clicked.connect(self.setup_telescope)

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
    
    def connect_telescope(self, b):
        if self.telescope_check_box.isChecked():
            name = "The telescope"
            self.setup_thread = TelescopeThread(self.parent.telescope, self)
            self.setup_thread.setup_complete.connect(self.telescope_settings)
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
        self.telescope_settings()
    
    def telescope_connect_failed(self, e: Exception):
        print(e)
        self.telescope_check_box.setChecked(False)
        self.parent.connect_fail_dialog("Telescope")
    
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
