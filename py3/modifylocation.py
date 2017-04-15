import sys
import os
import json
from PyQt5 import QtWidgets
import ui_modifylocation
import appglobals


class LocationDialog(QtWidgets.QDialog):
    def __init__(self):
        super(LocationDialog, self).__init__()
        self.location = {"Latitude": "00:00:00", "Longitude": "00:00:00"}
        if os.path.exists("location.json"):
            with open("location.json", "r") as f:
                self.location = json.load(f)
        self.lat = self.location["Latitude"].split(":")
        self.long = self.location["Longitude"].split(":")
        self.ui = ui_modifylocation.Ui_LocationDialog()

        self.ui.setupUi(self)
        self.setup_gui()

    def setup_gui(self):
        self.ui.lat_d_spin.setValue(int(self.lat[0]))
        self.ui.long_d_spin.setValue(int(self.long[0]))
        self.ui.lat_m_spin.setValue(int(self.lat[1]))
        self.ui.long_m_spin.setValue(int(self.long[1]))
        self.ui.lat_s_spin.setValue(int(self.lat[2]))
        self.ui.long_s_spin.setValue(int(self.long[2]))
        self.ui.button_box.accepted.connect(self.ok)
        self.ui.button_box.rejected.connect(self.cancel)

    # Do if "OK" button is pressed
    def ok(self):
        self.accept()
        self.latitude = str(self.ui.lat_d_spin.value()) + ":" + str(self.ui.lat_m_spin.value()) + ":" + str(self.ui.lat_s_spin.value())
        self.longitude = str(self.ui.long_d_spin.value()) + ":" + str(self.ui.long_m_spin.value()) + ":" + str(self.ui.long_s_spin.value())

        if os.path.exists("location.json"):
            os.remove("location.json")
        location_dict = {}
        location_dict.update({"Latitude": self.latitude})
        location_dict.update({"Longitude": self.longitude})
        with open("location.json", "a") as f:
            json.dump(location_dict, f, indent=0)

    # Do if "Cancel" button is pressed
    def cancel(self):
        self.reject()
