import json
import os
from PySide2 import QtCore, QtWidgets
import appglobals
from conversions import coordinates
from ui import ui_modifylocation


class LocationDialog(QtWidgets.QDialog, ui_modifylocation.Ui_LocationDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.dec_lat, self.dec_lon = coordinates.decimal_coordinates(appglobals.location["Latitude"],
                                                                     appglobals.location["Longitude"])

        self.setupUi(self)
        self.setup_gui()

    def setup_gui(self):
        self.lat_d_spin.setValue(appglobals.location["Latitude"][0])
        self.long_d_spin.setValue(appglobals.location["Longitude"][0])
        self.lat_m_spin.setValue(appglobals.location["Latitude"][1])
        self.long_m_spin.setValue(appglobals.location["Longitude"][1])
        self.lat_s_spin.setValue(appglobals.location["Latitude"][2])
        self.long_s_spin.setValue(appglobals.location["Longitude"][2])

        self.button_box.accepted.connect(self.ok)
        self.button_box.rejected.connect(self.cancel)

    def ok(self):
        """Do if "OK" button is pressed"""
        self.accept()
        appglobals.location["Latitude"] = [self.lat_d_spin.value(), self.lat_m_spin.value(), self.lat_s_spin.value()]
        appglobals.location["Longitude"] = [self.long_d_spin.value(), self.long_m_spin.value(),
                                            self.long_s_spin.value()]

        if os.path.exists("location.json"):
            os.remove("location.json")
        with open("location.json", "a") as f:
            json.dump(appglobals.location, f, indent=0)

    def cancel(self):
        """Do if "Cancel" button is pressed"""
        self.reject()
