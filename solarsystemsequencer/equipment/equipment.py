from abc import ABC, abstractmethod
from typing import Union


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


class FilterWheel(Device):
    @abstractmethod
    def wheel_position(self, pos: int): pass

    @abstractmethod
    def rotate_wheel(self, text: Union[str, int]): pass
