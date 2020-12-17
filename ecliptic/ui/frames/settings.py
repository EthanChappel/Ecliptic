import os
import json
from PySide2 import QtWidgets
from .uic.uic_settings import Ui_SettingsFrame
import appglobals


class SettingsFrame(QtWidgets.QFrame, Ui_SettingsFrame):
    def __init__(self, parent):
        self.parent = parent
        
        super().__init__(self.parent)
        self.setupUi(self)
        
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
