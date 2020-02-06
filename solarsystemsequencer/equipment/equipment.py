from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def device_name(self) -> str: pass

    @abstractmethod
    def is_connected(self) -> bool: pass

    @abstractmethod
    def set_connected(self, connected: bool): pass

    @abstractmethod
    def setup_dialog(self): pass
