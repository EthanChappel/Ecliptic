import os
import json
from typing import List, Tuple
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import ui_modifylocation


class LocationDialog(QtWidgets.QDialog):
    def __init__(self):
        super(LocationDialog, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        try:
            with open("location.json", "r") as f:
                self.location = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.location = {"Latitude": "00:00:00", "Longitude": "00:00:00"}
        self.lat = self.location["Latitude"].split(":")
        self.lon = self.location["Longitude"].split(":")
        self.dec_lat, self.dec_lon = self.decimal_coordinates([int(i) for i in self.lat], [int(i) for i in self.lon])

        self.earth_figure = plt.figure(facecolor=(0.333, 0.333, 0.333))
        self.earth_canvas = FigureCanvas(self.earth_figure)

        self.ui = ui_modifylocation.Ui_LocationDialog()
        self.ui.setupUi(self)
        self.setup_gui()

    def setup_gui(self):
        self.ui.lat_d_spin.setValue(int(self.lat[0]))
        self.ui.long_d_spin.setValue(int(self.lon[0]))
        self.ui.lat_m_spin.setValue(int(self.lat[1]))
        self.ui.long_m_spin.setValue(int(self.lon[1]))
        self.ui.lat_s_spin.setValue(int(self.lat[2]))
        self.ui.long_s_spin.setValue(int(self.lon[2]))

        self.ui.lat_d_spin.valueChanged.connect(lambda: self.generate_map())
        self.ui.long_d_spin.valueChanged.connect(lambda: self.generate_map())
        self.ui.lat_m_spin.valueChanged.connect(lambda: self.generate_map())
        self.ui.long_m_spin.valueChanged.connect(lambda: self.generate_map())
        self.ui.lat_s_spin.valueChanged.connect(lambda: self.generate_map())
        self.ui.long_s_spin.valueChanged.connect(lambda: self.generate_map())
        self.ui.button_box.accepted.connect(self.ok)
        self.ui.button_box.rejected.connect(self.cancel)

        self.generate_map()
        self.ui.earth_layout.addWidget(self.earth_canvas)

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
        self.lat = [self.ui.lat_d_spin.value(), self.ui.lat_m_spin.value(), self.ui.lat_s_spin.value()]
        self.lon = [self.ui.long_d_spin.value(), self.ui.long_m_spin.value(), self.ui.long_s_spin.value()]
        self.dec_lat, self.dec_lon = self.decimal_coordinates([int(i) for i in self.lat], [int(i) for i in self.lon])
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
        self.latitude = str(self.ui.lat_d_spin.value()) + ":" + str(self.ui.lat_m_spin.value()) + ":" + str(
            self.ui.lat_s_spin.value())
        self.longitude = str(self.ui.long_d_spin.value()) + ":" + str(self.ui.long_m_spin.value()) + ":" + str(
            self.ui.long_s_spin.value())

        if os.path.exists("location.json"):
            os.remove("location.json")
        location_dict = {}
        location_dict.update({"Latitude": self.latitude})
        location_dict.update({"Longitude": self.longitude})
        with open("location.json", "a") as f:
            json.dump(location_dict, f, indent=0)
        self.earth_figure.clf()

    def cancel(self):
        """Do if "Cancel" button is pressed"""
        self.reject()
        self.earth_figure.clf()

    def closeEvent(self, event):
        self.earth_figure.clf()
