import json
from PyQt5 import QtWidgets

telescope = None
camera = None
guider = None
wheel = None
focuser = None

targets_tuple = ("Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")

try:
    with open("location.json", "r") as f:
            location = json.load(f)
except FileNotFoundError:
    location = {"Latitude": [0, 0, 0], "Longitude": [0, 0, 0]}
except json.decoder.JSONDecodeError:
    messagebox = QtWidgets.QMessageBox()
    messagebox.setText("The location data seems to be broken. Coordinates will be set to 0°N 0°E.")
    messagebox.setIcon(QtWidgets.QMessageBox.Information)
    messagebox.exec_()
    location = {"Latitude": [0, 0, 0], "Longitude": [0, 0, 0]}
