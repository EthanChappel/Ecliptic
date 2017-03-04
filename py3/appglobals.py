import os
import json
from PyQt5 import QtCore

devices = {}
telescope = None
camera = None
guider = None
wheel = None
focuser = None

targets_tuple = ("Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")

telescope_thread = QtCore.QThread()
autoguide_thread = QtCore.QThread()
camera_thread = QtCore.QThread()
filterwheel_thread = QtCore.QThread()
focuser_thread = QtCore.QThread()

if os.path.exists("location.json"):
    with open("location.json", "r") as f:
        try:
            location = json.load(f)
        except json.decoder.JSONDecodeError:
            location = {'Latitude': 0.0, 'Longitude': 0.0}
