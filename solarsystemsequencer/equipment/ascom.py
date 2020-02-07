import os
import json
from typing import List, Union
import numpy as np
import appglobals
from equipment.equipment import Device, Telescope, Camera, FilterWheel, Focuser
import clr
clr.AddReference("ASCOM.DriverAccess, Version=6.0.0.0, Culture=neutral, PublicKeyToken=565de7938946fba7, processorArchitecture=MSIL")
clr.AddReference("ASCOM.Utilities, Version=6.0.0.0, Culture=neutral, PublicKeyToken=565de7938946fba7, processorArchitecture=MSIL")
import ASCOM.DriverAccess
import ASCOM.Utilities


class AscomDevice(Device):
    _device_type = None

    def __init__(self, device: type):
        self.device = device(self.chooser(type(self)._device_type))
        self.connect()

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

    @staticmethod
    def chooser(device_type: str) -> str:
        choose_dialog = ASCOM.Utilities.Chooser()
        choose_dialog.DeviceType = device_type
        return choose_dialog.Choose()


class AscomTelescope(Telescope, AscomDevice):
    _device_type = "Telescope"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.Telescope)

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


class AscomCamera(Camera, AscomDevice):
    _device_type = "Camera"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.Camera)

    def min_gain(self) -> int:
        return self.device.GainMin

    def max_gain(self) -> int:
        return self.device.GainMax

    def gain(self) -> int:
        return self.device.Gain

    def min_exposure(self) -> float:
        return self.device.ExposureMin

    def max_exposure(self) -> float:
        return self.device.ExposureMax

    def image_width(self) -> int:
        return self.device.NumX

    def image_height(self) -> int:
        return self.device.NumY

    def exposure_complete(self) -> bool:
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

    def exposure_progress(self) -> int:
        return self.device.PercentCompleted

    def image_array(self) -> List[int]:
        return list(self.device.ImageArray)


class AscomFilterWheel(FilterWheel, AscomDevice):
    _device_type = "FilterWheel"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.FilterWheel)

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


class AscomFocuser(Focuser, AscomDevice):
    _device_type = "Focuser"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.Focuser)

    def set_position(self, pos: int):
        self.device.Move(pos)

    def get_position(self) -> int:
        return self.device.Position

    def is_abs_position(self) -> bool:
        return self.device.Absolute

    def max_step(self) -> int:
        return self.device.MaxStep

    def is_temp_comp(self) -> bool:
        return self.device.TempComp

    def has_temp_comp(self) -> bool:
        return self.device.TempCompAvailable

    def set_temp_comp(self, val: bool):
        self.device.TempComp = val
