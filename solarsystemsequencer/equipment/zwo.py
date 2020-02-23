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
    def gain(self) -> int:
        return self._driver.get_control_value(asi.ASI_GAIN)[0]

    @gain.setter
    def gain(self, value: int):
        self._driver.set_control_value(asi.ASI_GAIN, value)

    @property
    def min_gain(self) -> int:
        return self._controls['Gain']['MinValue']

    @property
    def max_gain(self) -> int:
        return self._controls['Gain']['MaxValue']

    @property
    def has_gain(self) -> bool:
        return self._controls['Gain']['IsAutoSupported']

    @property
    def exposure(self) -> float:
        return self._driver.get_control_value(asi.ASI_EXPOSURE)[0]

    @exposure.setter
    def exposure(self, value: int):
        self._driver.set_control_value(asi.ASI_EXPOSURE, value)

    @property
    def min_exposure(self) -> float:
        return self._controls['Exposure']['MinValue']

    @property
    def max_exposure(self) -> float:
        return self._controls['Exposure']['MaxValue']

    @property
    def has_exposure(self) -> bool:
        return self._controls['Exposure']['IsAutoSupported']

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
    def has_bin(self) -> bool:
        # TODO: Determine if HardwareBin and Mono bin is correlated with color cameras
        if 'HardwareBin' in self._controls:
            return self._controls['HardwareBin']['IsAutoSupported']
        elif 'Mono bin' in self._controls:
            return self._controls['Mono bin']['IsAutoSupported']
        return False

    @property
    def exposure_complete(self) -> bool:
        return self._driver.get_exposure_status() == 2

    @property
    def name(self) -> str:
        return self._info['Name']

    @property
    def connected(self) -> bool:
        return True

    @property
    def bandwidth(self) -> int:
        return self._driver.get_control_value(asi.ASI_BANDWIDTHOVERLOAD)[0]

    @bandwidth.setter
    def bandwidth(self, value: int):
        self._driver.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, value)

    @property
    def min_bandwidth(self) -> int:
        return self._controls["BandWidth"]["MinValue"]

    @property
    def max_bandwidth(self) -> int:
        return self._controls["BandWidth"]["MaxValue"]

    @property
    def has_bandwidth(self) -> bool:
        return self._controls['BandWidth']['IsAutoSupported']

    @property
    def flip(self) -> int:
        return self._driver.get_control_value(asi.ASI_FLIP)[0]

    @flip.setter
    def flip(self, value: int):
        self._driver.set_control_value(asi.ASI_FLIP, value)

    @property
    def min_flip(self) -> int:
        return self._controls["Flip"]["MinValue"]

    @property
    def max_flip(self) -> int:
        return self._controls["Flip"]["MaxValue"]

    @property
    def has_flip(self) -> bool:
        return self._controls['Flip']['IsAutoSupported']

    @property
    def high_speed(self) -> bool:
        return self._driver.get_control_value(asi.ASI_HIGH_SPEED_MODE)[0]

    @high_speed.setter
    def high_speed(self, value: bool):
        self._driver.set_control_value(asi.ASI_HIGH_SPEED_MODE, value)

    @property
    def min_high_speed(self) -> bool:
        return self._controls['HighSpeedMode']['MinValue']

    @property
    def max_high_speed(self) -> bool:
        return self._controls['HighSpeedMode']['MaxValue']

    @property
    def has_high_speed(self) -> bool:
        return self._controls['HighSpeedMode']['IsAutoSupported']

    @property
    def temperature(self) -> float:
        return self._driver.get_control_value(asi.ASI_TEMPERATURE)[0]

    @property
    def min_temperature(self) -> float:
        return self._controls['Temperature']['MinValue']

    @property
    def max_temperature(self) -> float:
        return self._controls['Temperature']['MaxValue']

    @property
    def has_temperature(self) -> bool:
        return self._controls['Temperature']['IsAutoSupported']

    @property
    def target_temperature(self) -> float:
        return self._driver.get_control_value(asi.ASI_TARGET_TEMP)[0]

    @target_temperature.setter
    def target_temperature(self, value: float):
        self._driver.set_control_value(asi.ASI_TARGET_TEMP, value)

    @property
    def has_target_temperature(self) -> bool:
        try:
            t = self._driver.get_control_value(asi.ASI_TARGET_TEMP)[0]
            return True
        except asi.ZWO_IOError:
            return False

    @property
    def red_wb(self) -> int:
        return self._driver.get_control_value(asi.ASI_WB_R)[0]

    @red_wb.setter
    def red_wb(self, value: int):
        self._driver.set_control_value(asi.ASI_WB_R, value)

    @property
    def min_red_wb(self) -> int:
        return self._controls['WB_R']['MinValue']

    @property
    def max_red_wb(self) -> int:
        return self._controls['WB_R']['MaxValue']

    @property
    def has_red_wb(self) -> bool:
        if self._info["IsColorCam"]:
            return self._controls['WB_R']['IsAutoSupported']
        return False

    @property
    def blue_wb(self) -> int:
        return self._driver.get_control_value(asi.ASI_WB_B)[0]

    @blue_wb.setter
    def blue_wb(self, value: int):
        self._driver.set_control_value(asi.ASI_WB_B, value)

    @property
    def min_blue_wb(self) -> int:
        return self._controls['WB_B']['MinValue']

    @property
    def max_blue_wb(self) -> int:
        return self._controls['WB_B']['MaxValue']

    @property
    def has_blue_wb(self) -> bool:
        if self._info['IsColorCam']:
            return self._controls['WB_B']['IsAutoSupported']
        return False

    @property
    def is_color(self) -> bool:
        return self._info['IsColorCam']

    @property
    def has_usb3(self) -> bool:
        return self._info['IsUSB3Camera']

    @property
    def is_usb3_host(self) -> bool:
        return self._info['IsUSB3Host']

    @property
    def has_guide_port(self) -> bool:
        return self._info['ST4Port']

    @property
    def has_cooler(self) -> bool:
        return self._info['IsCoolerCam']
