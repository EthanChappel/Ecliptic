from abc import ABC, abstractmethod
from typing import Union
import numpy as np


class Device(ABC):
    @abstractmethod
    def device_name(self) -> str: pass

    @abstractmethod
    def is_connected(self) -> bool: pass

    @abstractmethod
    def set_connected(self, connected: bool): pass

    @abstractmethod
    def setup_dialog(self): pass


class Telescope(Device):
    @abstractmethod
    def goto(self, ra: float, dec: float): pass

    @abstractmethod
    def goto_home(self): pass

    @abstractmethod
    def move_axis(self, axis: int, rate: float): pass

    @abstractmethod
    def pulse_guide(self, direction: int, duration: int): pass

    @abstractmethod
    def set_parked(self, parked: bool): pass

    @abstractmethod
    def is_tracking(self) -> bool: pass

    @abstractmethod
    def set_tracking(self, tracking: bool): pass

    @abstractmethod
    def get_pier_side(self) -> int: pass


class Camera(Device):
    @abstractmethod
    def min_gain(self) -> int: pass

    @abstractmethod
    def max_gain(self) -> int: pass

    @abstractmethod
    def gain(self) -> int: pass

    @abstractmethod
    def min_exposure(self) -> float: pass

    @abstractmethod
    def max_exposure(self) -> float: pass

    @abstractmethod
    def image_width(self) -> int: pass

    @abstractmethod
    def image_height(self) -> int: pass

    @abstractmethod
    def exposure_complete(self) -> bool: pass

    @abstractmethod
    def capture(self, exposure: float, light: bool) -> np.ndarray: pass

    @abstractmethod
    def stop_exposure(self): pass

    @abstractmethod
    def exposure_progress(self) -> int: pass


class FilterWheel(Device):
    @abstractmethod
    def wheel_position(self, pos: int): pass

    @abstractmethod
    def rotate_wheel(self, text: Union[str, int]): pass


class Focuser(Device):
    @abstractmethod
    def set_position(self, pos: int): pass

    @abstractmethod
    def get_position(self) -> int: pass

    @abstractmethod
    def is_abs_position(self) -> bool: pass

    @abstractmethod
    def max_step(self) -> int: pass

    @abstractmethod
    def is_temp_comp(self) -> bool: pass

    @abstractmethod
    def has_temp_comp(self) -> bool: pass

    @abstractmethod
    def set_temp_comp(self, val: bool): pass
