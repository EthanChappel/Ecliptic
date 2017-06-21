from PyQt5 import QtWidgets
import zwoasi as asi
import ui_zwosettings


class ZWOSettings(QtWidgets.QFrame, ui_zwosettings.Ui_ZWOSettings):
    def __init__(self):
        super(ZWOSettings, self).__init__()
        self.camera = None
        self.setupUi(self)
        self.setup_gui()

    def setup_gui(self):
        self.temperature_spinbox.valueChanged.connect(self.set_temperature)
        self.brightness_spinbox.valueChanged.connect(self.set_brightness)
        self.gamma_spinbox.valueChanged.connect(self.set_gamma)
        self.red_spinbox.valueChanged.connect(self.set_red)
        self.blue_spinbox.valueChanged.connect(self.set_blue)
        self.usb_spinbox.valueChanged.connect(self.set_usb)

    def set_camera(self, camera: asi.Camera):
        self.camera = camera

    def set_temperature(self):
        temperature = int(self.temperature_spinbox.cleanText())
        self.camera.set_control_value(asi.ASI_TARGET_TEMP, temperature)

    def set_brightness(self):
        brightness = int(self.brightness_spinbox.cleanText())
        self.camera.set_control_value(asi.ASI_BRIGHTNESS, brightness)

    def set_gamma(self):
        gamma = int(self.gamma_spinbox.cleanText())
        self.camera.set_control_value(asi.ASI_GAMMA, gamma)

    def set_red(self):
        red = int(self.red_spinbox.cleanText())
        self.camera.set_control_value(asi.ASI_WB_R, red)

    def set_blue(self):
        blue = int(self.blue_spinbox.cleanText())
        self.camera.set_control_value(asi.ASI_WB_B, blue)

    def set_usb(self):
        usb = int(self.usb_spinbox.cleanText())
        self.camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, usb)
