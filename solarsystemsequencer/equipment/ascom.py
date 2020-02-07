import os
import json
from typing import List, Union
import numpy as np
import appglobals
from equipment.equipment import Device, Telescope, FilterWheel
import clr
clr.AddReference("ASCOM.DriverAccess, Version=6.0.0.0, Culture=neutral, PublicKeyToken=565de7938946fba7, processorArchitecture=MSIL")
clr.AddReference("ASCOM.Utilities, Version=6.0.0.0, Culture=neutral, PublicKeyToken=565de7938946fba7, processorArchitecture=MSIL")
import ASCOM.DriverAccess
import ASCOM.Utilities


class AscomDevice(Device):
    def __init__(self, device):
        self.device = None
        self.choose_dialog = ASCOM.Utilities.Chooser()
        self.choose_dialog.DeviceType = device
        self.choose = self.choose_dialog.Choose()

    def device_name(self) -> str:
        return self.device.Name

    def set_connected(self, connected: bool):
        self.device.Connected = connected

    def connect(self):
        self.set_connected(True)

    def disconnect(self):
        self.set_connected(False)

    def is_connected(self) -> bool:
        return self.device.Connected

    def dispose(self):
        self.device.Dispose()
        del self.device

    def setup_dialog(self):
        self.device.SetupDialog()


class AscomTelescope(Telescope, AscomDevice):
    def __init__(self):
        super().__init__("Telescope")
        self.device = ASCOM.DriverAccess.Telescope(self.choose)

    def can_slew_eq(self) -> bool:
        return self.device.CanSlew

    def can_slew_alt_az(self) -> bool:
        return self.device.CanSlewAltAz

    def goto_home(self):
        self.device.Unpark()
        self.device.FindHome()

    def set_parked(self, parked: bool):
        if parked:
            self.device.Park()
        else:
            self.device.Unpark()

    def is_tracking(self) -> bool:
        return self.device.Tracking

    def set_tracking(self, tracking: bool):
        self.device.Tracking = tracking

    def can_slew(self) -> bool:
        return self.device.CanSlew

    def goto(self, ra, dec):
        self.device.Tracking = True
        self.device.SlewToCoordinates(ra, dec)

    def move_axis(self, axis: int, rate: float):
        self.device.Tracking = True
        self.device.MoveAxis(axis, rate)

    def pulse_guide(self, direction: int, duration: int):
        self.device.PulseGuide(direction, duration)

    def get_pier_side(self):
        return self.device.SideOfPier


class Camera(AscomDevice):
    def __init__(self):
        super().__init__("Camera")
        self.device = ASCOM.DriverAccess.Camera(self.choose)
        self.connect()

    def gain_min(self) -> int:
        return self.device.GainMin

    def gain_max(self) -> int:
        return self.device.GainMax

    def gain(self) -> int:
        return self.device.Gain

    def exposure_min(self) -> float:
        return self.device.ExposureMin

    def exposure_max(self) -> float:
        return self.device.ExposureMax

    def num_x(self) -> int:
        return self.device.NumX

    def num_y(self) -> int:
        return self.device.NumY

    def image_ready(self) -> bool:
        return self.device.ImageReady

    def capture(self, exposure: float, light: bool) -> np.ndarray:
        self.device.StartExposure(exposure, light)
        while not self.device.ImageReady:
            pass
        image = self.device.ImageArray
        width, height = self.device.NumX, self.device.NumY
        image = np.asarray(list(image), dtype=np.uint8).reshape(width, height)  # list(image) is slow
        image = np.rot90(image, 1)
        image = np.flipud(image)
        return image

    def stop_exposure(self):
        self.device.StopExposure()

    def percent_completed(self) -> int:
        return self.device.PercentCompleted

    def image_array(self) -> List[int]:
        return list(self.device.ImageArray)


class AscomFilterWheel(FilterWheel, AscomDevice):
    def __init__(self):
        super().__init__("FilterWheel")
        self.device = ASCOM.DriverAccess.FilterWheel(self.choose)
        self.connect()

    def wheel_position(self, pos: int):
        self.device.Position = pos

    def rotate_wheel(self, text: Union[str, int]):
        try:
            self.device.Position = text
        except Exception:
            for f in appglobals.filters:
                if f["Name"] == text:
                    wheel_pos = f["Wheel Position"]
                    try:
                        self.device.Position = wheel_pos
                        break
                    except Exception:
                        pass


class Focuser(AscomDevice):
    def __init__(self):
        super().__init__("Focuser")
        self.device = ASCOM.DriverAccess.Focuser(self.choose)
        self.connect()

    def move(self, pos: int):
        self.device.Move(pos)

    def position(self) -> int:
        return self.device.Position

    def absolute(self) -> bool:
        return self.device.Absolute

    def max_step(self) -> int:
        return self.device.MaxStep

    def is_temp_comp(self) -> bool:
        return self.device.TempComp

    def temp_comp_available(self) -> bool:
        return self.device.TempCompAvailable

    def temp_comp(self, val: bool):
        self.device.TempComp = val
