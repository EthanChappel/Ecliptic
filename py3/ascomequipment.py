import os
import json
from PIL import Image
import numpy as np
import clr
clr.AddReference("ASCOM.DriverAccess")
clr.AddReference("ASCOM.Utilities")
import ASCOM.DriverAccess
import ASCOM.Utilities
from System import Array


class Device():
    def __init__(self, device):
        super(Device, self).__init__()
        self.device = device
        self.choose_dialog = ASCOM.Utilities.Chooser()
        self.choose_dialog.DeviceType = device
        self.choose = self.choose_dialog.Choose()

    def name_(self):
        return self.device.Name

    def connect(self):
        self.device.Connected = True

    def connected(self):
        return self.device.Connected

    def disconnect(self):
        self.device.Connected = False

    def dispose(self):
        self.device.Dispose()
        del self.device

    def setup_dialog(self):
        self.device.SetupDialog()


class Telescope(Device):
    def __init__(self):
        super(Telescope, self).__init__("Telescope")
        self.device = ASCOM.DriverAccess.Telescope(self.choose)

    def canslew_eq(self):
        return self.device.CanSlew

    def canslew_altaz(self):
        return self.device.CanSlewAltAz

    def home(self):
        self.device.Unpark()
        self.device.FindHome()

    def park(self):
        self.device.Park()

    def can_slew(self):
        return self.device.CanSlew

    def stop_tracking(self):
        self.device.Tracking = False

    def goto(self, ra, dec):
        self.device.Tracking = True
        self.device.SlewToCoordinates(ra, dec)

    def move_axis(self, axis, rate):
        self.device.Tracking = True
        self.device.MoveAxis(axis, rate)


class Camera(Device):
    def __init__(self):
        super(Camera, self).__init__("Camera")
        self.device = ASCOM.DriverAccess.Camera(self.choose)
        self.connect()

    def gain_min(self):
        return self.device.GainMin

    def gain_max(self):
        return self.device.GainMax

    def gain(self):
        return self.device.Gain

    def exposure_min(self):
        return self.device.ExposureMin

    def exposure_max(self):
        return self.device.ExposureMax

    def num_x(self):
        return self.device.NumX

    def num_y(self):
        return self.device.NumY

    def image_ready(self):
        return self.device.ImageReady

    def capture(self, exposure, light):
        print(0)
        self.device.StartExposure(exposure, light)
        print(1)
        while not self.device.ImageReady:
            pass
        print(2)
        image = self.device.ImageArray
        print(3)
        width, height = self.device.NumX, self.device.NumY
        print(4)
        image = np.asarray(list(image), dtype=np.uint8).reshape(width, height)
        print(5)
        image = np.rot90(image, 1)
        print(6)
        image = np.flipud(image)
        print(8)
        return image

    def stop_exposure(self):
        self.device.StopExposure()

    def percent_completed(self):
        return self.device.PercentCompleted

    def image_array(self):
        image = list(self.device.ImageArray)
        return image


class FilterWheel(Device):
    def __init__(self):
        super(FilterWheel, self).__init__("FilterWheel")
        self.device = ASCOM.DriverAccess.FilterWheel(self.choose)
        self.connect()
        if os.path.exists("filters.json"):
            with open("filters.json", "r") as f:
                self.filters = json.load(f)

    def wheel_position(self, pos):
        self.device.Position = pos

    def rotate_wheel(self, text):
        try:
            self.device.Position = text
        except Exception:
            for f in self.filters:
                if f["Name"] == text:
                    wheel_pos = f["Wheel Position"]
                    try:
                        self.device.Position = wheel_pos
                        break
                    except Exception:
                        pass


class Focuser(Device):
    def __init__(self):
        super(Focuser, self).__init__("Focuser")
        self.device = ASCOM.DriverAccess.Focuser(self.choose)
        self.connect()

    def move(self, pos):
        self.device.Move(pos)

    def position(self):
        return self.device.Position

    def absolute(self):
        return self.device.Absolute

    def max_step(self):
        return self.device.MaxStep

    def is_temp_comp(self):
        return self.device.TempComp

    def temp_comp_available(self):
        return self.device.TempCompAvailable

    def temp_comp(self, val):
        self.device.TempComp = val
