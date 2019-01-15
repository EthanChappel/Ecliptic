import zwoasi as asi
from PySide2 import QtWidgets
from ui import ui_zwosettings


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

    def setup_controls(self, values):
        if "Gamma" in values:
            self.gamma_label.setVisible(True)
            self.gamma_spinbox.setVisible(True)
            self.gamma_spinbox.setMinimum(values["Gamma"]["Min"])
            self.gamma_spinbox.setMaximum(values["Gamma"]["Max"])
            self.gamma_spinbox.setValue(values["Gamma"]["Current"])
        else:
            self.gamma_label.setVisible(False)
            self.gamma_spinbox.setVisible(False)

        if "Brightness" in values:
            self.brightness_label.setVisible(True)
            self.brightness_spinbox.setVisible(True)
            self.brightness_spinbox.setMinimum(values["Brightness"]["Min"])
            self.brightness_spinbox.setMaximum(values["Brightness"]["Max"])
            self.brightness_spinbox.setValue(values["Brightness"]["Current"])
        else:
            self.brightness_label.setVisible(False)
            self.brightness_spinbox.setVisible(False)

        if "Bandwidth" in values:
            self.usb_label.setVisible(True)
            self.usb_spinbox.setVisible(True)
            self.usb_spinbox.setMinimum(values["Bandwidth"]["Min"])
            self.usb_spinbox.setMaximum(values["Bandwidth"]["Max"])
            self.usb_spinbox.setValue(values["Bandwidth"]["Current"])
        else:
            self.usb_label.setVisible(False)
            self.usb_spinbox.setVisible(False)

        if "Flip" in values:
            self.horizontalflip_checkbox.setVisible(True)
            self.verticalflip_checkbox.setVisible(True)
            if values["Flip"]["Current"] == 0:
                self.horizontalflip_checkbox.setChecked(False)
                self.verticalflip_checkbox.setChecked(False)
            elif values["Flip"]["Current"] == 1:
                self.horizontalflip_checkbox.setChecked(True)
                self.verticalflip_checkbox.setChecked(False)
            elif values["Flip"]["Current"] == 2:
                self.horizontalflip_checkbox.setChecked(False)
                self.verticalflip_checkbox.setChecked(True)
            elif values["Flip"]["Current"] == 3:
                self.horizontalflip_checkbox.setChecked(True)
                self.verticalflip_checkbox.setChecked(True)
        else:
            self.horizontalflip_checkbox.setVisible(False)
            self.verticalflip_checkbox.setVisible(False)

        if "High Speed" in values:
            self.highspeed_checkbox.setVisible(True)
            if values["High Speed"]["Current"] == 0:
                self.highspeed_checkbox.setChecked(False)
            elif values["High Speed"]["Current"] == 1:
                self.highspeed_checkbox.setChecked(True)
        else:
            self.highspeed_checkbox.setVisible(False)

        if "Temperature" in values:
            self.temperature_label.setVisible(True)
            self.temperature_spinbox.setVisible(True)
            self.temperature_spinbox.setMinimum(values["Temperature"]["Min"])
            self.temperature_spinbox.setMaximum(values["Temperature"]["Max"])
            self.temperature_spinbox.setValue(values["Temperature"]["Current"])
        else:
            self.temperature_label.setVisible(False)
            self.temperature_spinbox.setVisible(False)

        if "Red" in values:
            self.red_label.setVisible(True)
            self.red_spinbox.setVisible(True)
            self.red_spinbox.setMinimum(values["Red"]["Min"])
            self.red_spinbox.setMaximum(values["Red"]["Max"])
            self.red_spinbox.setValue(values["Red"]["Current"])
        else:
            self.red_label.setVisible(False)
            self.red_spinbox.setVisible(False)

        if "Blue" in values:
            self.blue_label.setVisible(True)
            self.blue_spinbox.setVisible(True)
            self.blue_spinbox.setMinimum(values["Blues"]["Min"])
            self.blue_spinbox.setMaximum(values["Blues"]["Max"])
            self.blue_spinbox.setValue(values["Blues"]["Current"])
        else:
            self.blue_label.setVisible(False)
            self.blue_spinbox.setVisible(False)

        if "Hardware Bin" in values:
            self.hardwarebin_checkbox.setVisible(True)
            if values["Hardware Bin"]["Current"] == 0:
                self.hardwarebin_checkbox.setChecked(False)
            elif values["Hardware Bin"]["Current"] == 1:
                self.hardwarebin_checkbox.setChecked(True)
        else:
            self.hardwarebin_checkbox.setVisible(False)

        if "Mono Bin" in values:
            self.monobin_checkbox.setVisible(True)
            if values["Mono Bin"]["Current"] == 0:
                self.monobin_checkbox.setChecked(False)
            if values["Mono Bin"]["Current"] == 1:
                self.monobin_checkbox.setChecked(True)
        else:
            self.monobin_checkbox.setVisible(False)

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
