import os
import json
from typing import List, Tuple
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import ui_modifylocation
import appglobals


class LocationDialog(QtWidgets.QDialog, ui_modifylocation.Ui_LocationDialog):
    def __init__(self):
        super(LocationDialog, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.dec_lat, self.dec_lon = self.decimal_coordinates(appglobals.location["Latitude"],
                                                              appglobals.location["Longitude"])

        self.earth_figure = plt.figure(facecolor=(0.333, 0.333, 0.333))
        self.earth_canvas = FigureCanvas(self.earth_figure)

        self.setupUi(self)
        self.setup_gui()

    def setup_gui(self):
        self.lat_d_spin.setValue(appglobals.location["Latitude"][0])
        self.long_d_spin.setValue(appglobals.location["Longitude"][0])
        self.lat_m_spin.setValue(appglobals.location["Latitude"][1])
        self.long_m_spin.setValue(appglobals.location["Longitude"][1])
        self.lat_s_spin.setValue(appglobals.location["Latitude"][2])
        self.long_s_spin.setValue(appglobals.location["Longitude"][2])

        self.lat_d_spin.valueChanged.connect(self.generate_map)
        self.long_d_spin.valueChanged.connect(self.generate_map)
        self.lat_m_spin.valueChanged.connect(self.generate_map)
        self.long_m_spin.valueChanged.connect(self.generate_map)
        self.lat_s_spin.valueChanged.connect(self.generate_map)
        self.long_s_spin.valueChanged.connect(self.generate_map)
        self.button_box.accepted.connect(self.ok)
        self.button_box.rejected.connect(self.cancel)

        self.generate_map()
        self.earth_layout.addWidget(self.earth_canvas)

    def decimal_coordinates(self, lat: List[int], lon: List[int]) -> Tuple[float, float]:
        """Convert coordinates in ###:##:## format to floats."""
        if int(lat[0]) < 0:
            lat_dec = int(lat[0]) + (-1 * (float(lat[1]) / 60)) + (-1 * (float(lat[2]) / 3600))
        else:
            lat_dec = int(lat[0]) + (float(lat[1]) / 60) + (float(lat[2]) / 3600)
        if int(lon[0]) < 0:
            lon_dec = int(lon[0]) + (-1 * (float(lon[1]) / 60)) + (-1 * (float(lon[2]) / 3600))
        else:
            lon_dec = int(lon[0]) + (float(lon[1]) / 60) + (float(lon[2]) / 3600)
        return lat_dec, lon_dec

    def generate_map(self):
        """Generate map to display in window."""
        # TODO: Fix map shrinking on first change
        self.earth_figure.clf()
        appglobals.location["Latitude"] = [self.lat_d_spin.value(), self.lat_m_spin.value(), self.lat_s_spin.value()]
        appglobals.location["Longitude"] = [self.long_d_spin.value(), self.long_m_spin.value(), self.long_s_spin.value()]
        self.dec_lat, self.dec_lon = self.decimal_coordinates(appglobals.location["Latitude"],
                                                              appglobals.location["Longitude"])
        earth_axes = plt.axes(projection=ccrs.Orthographic(self.dec_lon, self.dec_lat))
        earth_axes.add_feature(cfeature.LAND, facecolor="white")
        earth_axes.add_feature(cfeature.LAKES, edgecolor="black", facecolor="white")
        earth_axes.add_feature(cfeature.RIVERS, edgecolor="black")
        earth_axes.set_global()
        earth_axes.plot(self.dec_lon, self.dec_lat, 'ro', markersize=4)
        # earth_axes.add_feature(cfeature.OCEAN, facecolor="white")
        earth_axes.add_feature(cfeature.COASTLINE)
        self.earth_figure.add_subplot(earth_axes)
        self.earth_figure.tight_layout()
        self.earth_canvas.draw()

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
        self.earth_figure.clf()

    def cancel(self):
        """Do if "Cancel" button is pressed"""
        self.reject()
        self.earth_figure.clf()

    def closeEvent(self, event):
        self.earth_figure.clf()
