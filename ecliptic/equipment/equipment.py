from abc import ABC, abstractmethod
from typing import Union
import numpy as np


class Device(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass

    @property
    @abstractmethod
    def connected(self): pass

    @connected.setter
    @abstractmethod
    def connected(self, value: bool): pass

    @abstractmethod
    def close(self): pass


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

    @property
    @abstractmethod
    def tracking(self) -> bool: pass

    @tracking.setter
    @abstractmethod
    def tracking(self, value: bool): pass

    @property
    @abstractmethod
    def right_ascension(self) -> float: pass

    @property
    @abstractmethod
    def declination(self) -> float: pass

    @property
    @abstractmethod
    def pier_side(self) -> int: pass


class Camera(Device):
    @property
    @abstractmethod
    def video_mode(self):
        return None

    @video_mode.setter
    @abstractmethod
    def video_mode(self, value: bool):
        pass

    @abstractmethod
    def get_frame(self) -> np.ndarray: pass

    @abstractmethod
    def stop_exposure(self): pass

    @property
    @abstractmethod
    def gain(self) -> int: pass

    @gain.setter
    @abstractmethod
    def gain(self, value: int): pass

    @property
    @abstractmethod
    def min_gain(self) -> int: pass

    @property
    @abstractmethod
    def max_gain(self) -> int: pass

    @property
    @abstractmethod
    def exposure(self) -> float: pass

    @property
    @abstractmethod
    def has_gain(self) -> bool: pass

    @exposure.setter
    @abstractmethod
    def exposure(self, value: int): pass

    @property
    @abstractmethod
    def min_exposure(self) -> float: pass

    @property
    @abstractmethod
    def max_exposure(self) -> float: pass

    @property
    @abstractmethod
    def has_exposure(self) -> bool: pass

    @property
    @abstractmethod
    def roi_resolution(self): pass

    @abstractmethod
    def set_roi_resolution(self, width: int, height: int): pass

    @property
    @abstractmethod
    def roi_offset(self): pass

    @abstractmethod
    def set_roi_offset(self, x: int, y: int): pass

    @property
    @abstractmethod
    def bin(self) -> int: pass

    @bin.setter
    @abstractmethod
    def bin(self, value: int): pass

    @property
    @abstractmethod
    def exposure_complete(self) -> bool: pass

    @property
    @abstractmethod
    def high_speed(self) -> bool: pass

    @high_speed.setter
    @abstractmethod
    def high_speed(self, value: bool): pass

    @property
    @abstractmethod
    def min_high_speed(self) -> bool: pass

    @property
    @abstractmethod
    def max_high_speed(self) -> bool: pass

    @property
    @abstractmethod
    def has_high_speed(self) -> bool: pass

    @property
    @abstractmethod
    def temperature(self) -> float: pass

    @property
    @abstractmethod
    def min_temperature(self) -> float: pass

    @property
    @abstractmethod
    def max_temperature(self) -> float: pass

    @property
    @abstractmethod
    def has_temperature(self) -> bool: pass

    @property
    @abstractmethod
    def target_temperature(self) -> float: pass

    @target_temperature.setter
    @abstractmethod
    def target_temperature(self, value: float): pass

    @property
    @abstractmethod
    def has_target_temperature(self) -> bool: pass


class FilterWheel(Device):
    @property
    @abstractmethod
    def position(self): pass

    @position.setter
    @abstractmethod
    def position(self, value: int): pass

    @abstractmethod
    def rotate_wheel(self, text: Union[str, int]): pass


class Focuser(Device):

    @abstractmethod
    def is_abs_position(self) -> bool: pass

    @abstractmethod
    def has_temp_comp(self) -> bool: pass

    @property
    @abstractmethod
    def position(self) -> int: pass

    @position.setter
    @abstractmethod
    def position(self, value: int): pass

    @property
    @abstractmethod
    def max_step(self) -> int: pass

    @property
    @abstractmethod
    def temp_comp(self) -> bool: pass

    @temp_comp.setter
    @abstractmethod
    def temp_comp(self, value: bool): pass
