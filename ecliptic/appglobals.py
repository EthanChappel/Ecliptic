import json
from PySide6 import QtWidgets

targets_tuple = ("Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")

try:
    with open("settings.json", "r") as f:
            settings = json.load(f)
except FileNotFoundError:
    settings = {}
except json.decoder.JSONDecodeError:
    messagebox = QtWidgets.QMessageBox()
    messagebox.setText("The settings data seems to be broken.")
    messagebox.setIcon(QtWidgets.QMessageBox.Information)
    messagebox.exec_()
    settings = {}

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

try:
    with open("filters.json", "r") as f:
        filters = json.load(f)
except FileNotFoundError:
    filters = []
except json.decoder.JSONDecodeError:
    messagebox = QtWidgets.QMessageBox()
    messagebox.setText("The filters data seems to be broken.")
    messagebox.setIcon(QtWidgets.QMessageBox.Information)
    messagebox.exec_()
    filters = []
