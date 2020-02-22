import numpy as np
import zwoasi as asi
from equipment.equipment import Camera


class ZwoCamera(Camera):
    def __init__(self, index: int, image_type: int = asi.ASI_IMG_RAW16):
        self.image_type = image_type
        self._driver = asi.Camera(index)
        self._controls = self._driver.get_controls()
        self._info = self._driver.get_camera_property()

    @property
    def video_mode(self) -> bool:
        try:
            self._driver.capture_video_frame()
            return True
        except asi.ZWO_Error:
            return False

    @video_mode.setter
    def video_mode(self, value: bool):
        if value:
            self._driver.start_video_capture()
        else:
            self._driver.stop_video_capture()

    def get_frame(self) -> np.ndarray:
        return self._driver.capture_video_frame(timeout=int(self.exposure * 2 + 500))

    def stop_exposure(self):
        self._driver.stop_exposure()

    @property
    def min_gain(self) -> int:
        return self._controls["Gain"]["MinValue"]

    @property
    def max_gain(self) -> int:
        return self._controls["Gain"]["MaxValue"]

    @property
    def gain(self) -> int:
        return self._driver.get_control_value(asi.ASI_GAIN)[0]

    @gain.setter
    def gain(self, value: int):
        self._driver.set_control_value(asi.ASI_GAIN, value)

    @property
    def min_exposure(self) -> float:
        return self._controls["Exposure"]["MinValue"]

    @property
    def max_exposure(self) -> float:
        return self._controls["Exposure"]["MaxValue"]

    @property
    def exposure(self) -> float:
        return self._driver.get_control_value(asi.ASI_EXPOSURE)[0]

    @exposure.setter
    def exposure(self, value: int):
        self._driver.set_control_value(asi.ASI_EXPOSURE, value)

    @property
    def roi_resolution(self):
        return self._driver.get_roi()[:2]

    def set_roi_resolution(self, width: int, height: int):
        self._driver.set_roi_format(width, height, self.bin, self.image_type)

    @property
    def roi_offset(self):
        return self._driver.get_roi_start_position()

    def set_roi_offset(self, x: int, y: int):
        self._driver.set_roi_start_position(x, y)

    @property
    def bin(self):
        return self._driver.get_bin()

    @bin.setter
    def bin(self, value: int):
        f = self._driver.get_roi_format()[:2]
        self._driver.set_roi_format(*f, value, self.image_type)

    @property
    def exposure_complete(self) -> bool:
        return self._driver.get_exposure_status() == 2

    @property
    def name(self) -> str:
        return self._info['Name']

    @property
    def connected(self):
        return True
