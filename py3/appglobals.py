import os
import json

telescope = None
camera = None
guider = None
wheel = None
focuser = None

targets_tuple = ("Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")

if os.path.exists("location.json"):
    with open("location.json", "r") as f:
        try:
            location = json.load(f)
        except json.decoder.JSONDecodeError:
            location = {'Latitude': 0.0, 'Longitude': 0.0}
