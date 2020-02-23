from typing import List, Union
import numpy as np
import appglobals
from equipment.equipment import Device, Telescope, Camera, FilterWheel, Focuser
import clr
clr.AddReference("ASCOM.DriverAccess, Version=6.0.0.0, Culture=neutral, PublicKeyToken=565de7938946fba7, processorArchitecture=MSIL")
clr.AddReference("ASCOM.Exceptions, Version=6.0.0.0, Culture=neutral, PublicKeyToken=565de7938946fba7, processorArchitecture=MSIL")
clr.AddReference("ASCOM.Utilities, Version=6.0.0.0, Culture=neutral, PublicKeyToken=565de7938946fba7, processorArchitecture=MSIL")
import ASCOM


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
        self._exposure = 0
        self._target_temperature = None

    def get_frame(self) -> np.ndarray:
        self.driver.StartExposure(self.exposure / 1000, True)
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

    @property
    def gain(self) -> int:
        return self.driver.Gain

    @gain.setter
    def gain(self, value: int):
        self.driver.Gain = value

    @property
    def min_gain(self) -> int:
        return self.driver.GainMin

    @property
    def max_gain(self) -> int:
        return self.driver.GainMax

    @property
    def has_gain(self) -> bool:
        try:
            self.driver.Gain
            return True
        except ASCOM.Exceptions.PropertyNotImplementedException:
            return False

    @property
    def exposure(self) -> float:
        return self._exposure

    @exposure.setter
    def exposure(self, value: float):
        self._exposure = value

    @property
    def min_exposure(self) -> float:
        return self.driver.ExposureMin

    @property
    def max_exposure(self) -> float:
        return self.driver.ExposureMax

    @property
    def has_exposure(self) -> bool:
        return True

    @property
    def roi_resolution(self):
        return self.driver.NumX, self.driver.NumY

    def set_roi_resolution(self, width: int, height: int):
        self.driver.NumX = width
        self.driver.NumY = height

    @property
    def roi_offset(self):
        return self.driver.StartX, self.driver.StartY

    def set_roi_offset(self, x: int, y: int):
        self.driver.StartX = x
        self.driver.StartY = y

    @property
    def bin(self) -> int:
        return self.driver.BinX

    @property
    def exposure_complete(self) -> bool:
        return self.driver.ImageReady

    @property
    def exposure_progress(self) -> int:
        return self.driver.PercentCompleted

    @property
    def image_array(self) -> List[int]:
        return list(self.driver.ImageArray)

    @property
    def video_mode(self):
        return None

    @video_mode.setter
    def video_mode(self, value: bool):
        pass

    @property
    def high_speed(self) -> int:
        return self.driver.FastReadout

    @property
    def min_high_speed(self) -> int:
        if self.driver.CanFastReadout:
            return 0
        return None

    @property
    def max_high_speed(self) -> int:
        if self.driver.CanFastReadout:
            return 1
        return None

    @property
    def has_high_speed(self) -> bool:
        return self.driver.CanFastReadout

    @property
    def temperature(self) -> float:
        return self.driver.CCDTemperature

    @property
    def min_temperature(self) -> int:
        return None

    @property
    def max_temperature(self) -> int:
        return None

    @property
    def has_temperature(self) -> bool:
        return self.driver.SupportedActions

    @property
    def target_temperature(self) -> float:
        return self._target_temperature

    @target_temperature.setter
    def target_temperature(self, value: float):
        self._target_temperature = self.driver.SetCCDTemperature(value)

    @property
    def has_target_temperature(self) -> bool:
        return self.driver.CanSetCCDTemperature


class AscomFilterWheel(FilterWheel, AscomDevice):
    _device_type = "FilterWheel"

    def __init__(self):
        super().__init__(ASCOM.DriverAccess.FilterWheel)

    @property
    def position(self) -> int:
        return self.driver.Position

    @position.setter
    def position(self, value: int):
        self.driver.Position = value

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

    def is_abs_position(self) -> bool:
        return self.driver.Absolute

    def has_temp_comp(self) -> bool:
        return self.driver.TempCompAvailable

    @property
    def position(self) -> int:
        return self.driver.Position

    @position.setter
    def position(self, value: int):
        self.driver.Move(value)

    @property
    def max_step(self) -> int:
        return self.driver.MaxStep

    @property
    def temp_comp(self) -> bool:
        return self.driver.TempComp

    @temp_comp.setter
    def temp_comp(self, value: bool):
        self.driver.TempComp = value
