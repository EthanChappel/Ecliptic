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
        self.driver = device(self.chooser(type(self)._device_type))
        self.driver.Connected = True

    def dispose(self):
        self.driver.Dispose()
        del self.driver

    def setup_dialog(self):
        self.driver.SetupDialog()

    @staticmethod
    def chooser(device_type: str) -> str:
        choose_dialog = ASCOM.Utilities.Chooser()
        choose_dialog.DeviceType = device_type
        return choose_dialog.Choose()

    @property
    def name(self) -> str:
        return self.driver.Name

    @property
    def connected(self):
        return self.driver.Connected

    @connected.setter
    def connected(self, value: bool):
        self.driver.Connected = value


class AscomTelescope(Telescope, AscomDevice):
    _device_type = "Telescope"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.Telescope)

    def goto_home(self):
        self.driver.Unpark()
        self.driver.FindHome()

    def set_parked(self, parked: bool):
        if parked:
            self.driver.Park()
        else:
            self.driver.Unpark()

    def goto(self, ra, dec):
        self.driver.Tracking = True
        self.driver.SlewToCoordinates(ra, dec)

    def move_axis(self, axis: int, rate: float):
        self.driver.Tracking = True
        self.driver.MoveAxis(axis, rate)

    def pulse_guide(self, direction: int, duration: int):
        self.driver.PulseGuide(direction, duration)

    @property
    def can_slew_eq(self) -> bool:
        return self.driver.CanSlew

    @property
    def can_slew_alt_az(self) -> bool:
        return self.driver.CanSlewAltAz

    @property
    def tracking(self) -> bool:
        return self.driver.Tracking

    @tracking.setter
    def tracking(self, value: bool):
        self.driver.Tracking = value

    @property
    def can_slew(self) -> bool:
        return self.driver.CanSlew

    @property
    def pier_side(self):
        return self.driver.SideOfPier


class AscomCamera(Camera, AscomDevice):
    _device_type = "Camera"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.Camera)

    def min_gain(self) -> int:
        return self.driver.GainMin

    def max_gain(self) -> int:
        return self.driver.GainMax

    def gain(self) -> int:
        return self.driver.Gain

    def min_exposure(self) -> float:
        return self.driver.ExposureMin

    def max_exposure(self) -> float:
        return self.driver.ExposureMax

    def image_width(self) -> int:
        return self.driver.NumX

    def image_height(self) -> int:
        return self.driver.NumY

    def exposure_complete(self) -> bool:
        return self.driver.ImageReady

    def capture(self, exposure: float, light: bool) -> np.ndarray:
        self.driver.StartExposure(exposure, light)
        while not self.driver.ImageReady:
            pass
        image = self.driver.ImageArray
        width, height = self.driver.NumX, self.driver.NumY
        image = np.asarray(list(image), dtype=np.uint8).reshape(width, height)  # list(image) is slow
        image = np.rot90(image, 1)
        image = np.flipud(image)
        return image

    def stop_exposure(self):
        self.driver.StopExposure()

    def exposure_progress(self) -> int:
        return self.driver.PercentCompleted

    def image_array(self) -> List[int]:
        return list(self.driver.ImageArray)


class AscomFilterWheel(FilterWheel, AscomDevice):
    _device_type = "FilterWheel"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.FilterWheel)

    def wheel_position(self, pos: int):
        self.driver.Position = pos

    def rotate_wheel(self, text: Union[str, int]):
        try:
            self.driver.Position = text
        except Exception:
            for f in appglobals.filters:
                if f["Name"] == text:
                    wheel_pos = f["Wheel Position"]
                    try:
                        self.driver.Position = wheel_pos
                        break
                    except Exception:
                        pass


class AscomFocuser(Focuser, AscomDevice):
    _device_type = "Focuser"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.Focuser)

    def set_position(self, pos: int):
        self.driver.Move(pos)

    def get_position(self) -> int:
        return self.driver.Position

    def is_abs_position(self) -> bool:
        return self.driver.Absolute

    def max_step(self) -> int:
        return self.driver.MaxStep

    def is_temp_comp(self) -> bool:
        return self.driver.TempComp

    def has_temp_comp(self) -> bool:
        return self.driver.TempCompAvailable

    def set_temp_comp(self, val: bool):
        self.driver.TempComp = val
