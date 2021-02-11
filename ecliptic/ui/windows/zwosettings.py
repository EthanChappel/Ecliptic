from typing import Union
from PySide6 import QtWidgets
from equipment import zwo
from ui.windows.uic.uic_zwosettings import Ui_ZWOSettings


class ZWOSettings(QtWidgets.QFrame, Ui_ZWOSettings):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.setupUi(self)
        self.setup_gui()

    def setup_gui(self):
        self.temperature_spinbox.valueChanged.connect(self.set_temperature)
        self.red_spinbox.valueChanged.connect(self.set_red)
        self.blue_spinbox.valueChanged.connect(self.set_blue)
        self.usb_spinbox.valueChanged.connect(self.set_usb)

    def setup_controls(self, camera):
        if camera.has_bandwidth:
            self.usb_label.setVisible(True)
            self.usb_spinbox.setVisible(True)
            self.usb_spinbox.setMinimum(camera.min_bandwidth)
            self.usb_spinbox.setMaximum(camera.max_bandwidth)
            self.usb_spinbox.setValue(camera.bandwidth)
        else:
            self.usb_label.setVisible(False)
            self.usb_spinbox.setVisible(False)

        if camera.has_flip:
            self.horizontalflip_checkbox.setVisible(True)
            self.verticalflip_checkbox.setVisible(True)
            if camera.flip == 0:
                self.horizontalflip_checkbox.setChecked(False)
                self.verticalflip_checkbox.setChecked(False)
            elif camera.flip == 1:
                self.horizontalflip_checkbox.setChecked(True)
                self.verticalflip_checkbox.setChecked(False)
            elif camera.flip == 2:
                self.horizontalflip_checkbox.setChecked(False)
                self.verticalflip_checkbox.setChecked(True)
            elif camera.flip == 3:
                self.horizontalflip_checkbox.setChecked(True)
                self.verticalflip_checkbox.setChecked(True)
        else:
            self.horizontalflip_checkbox.setVisible(False)
            self.verticalflip_checkbox.setVisible(False)

        if camera.has_high_speed:
            self.highspeed_checkbox.setVisible(True)
            if camera.high_speed == 0:
                self.highspeed_checkbox.setChecked(False)
            elif camera.high_speed == 1:
                self.highspeed_checkbox.setChecked(True)
        else:
            self.highspeed_checkbox.setVisible(False)

        if camera.has_temperature:
            self.temperature_label.setVisible(True)
            self.temperature_spinbox.setVisible(True)
            self.temperature_spinbox.setMinimum(camera.min_temperature)
            self.temperature_spinbox.setMaximum(camera.max_temperature)
            self.temperature_spinbox.setValue(camera.temperature)
        else:
            self.temperature_label.setVisible(False)
            self.temperature_spinbox.setVisible(False)

        if camera.has_red_wb:
            self.red_label.setVisible(True)
            self.red_spinbox.setVisible(True)
            self.red_spinbox.setMinimum(camera.min_red_wb)
            self.red_spinbox.setMaximum(camera.max_red_wb)
            self.red_spinbox.setValue(camera.red_wb)
        else:
            self.red_label.setVisible(False)
            self.red_spinbox.setVisible(False)

        if camera.has_blue_wb:
            self.blue_label.setVisible(True)
            self.blue_spinbox.setVisible(True)
            self.blue_spinbox.setMinimum(camera.min_blue_wb)
            self.blue_spinbox.setMaximum(camera.max_blue_wb)
            self.blue_spinbox.setValue(camera.blue_wb)
        else:
            self.blue_label.setVisible(False)
            self.blue_spinbox.setVisible(False)

        if camera.has_bin:
            self.hardwarebin_checkbox.setVisible(True)
            if camera.bin == 0:
                self.hardwarebin_checkbox.setChecked(False)
            elif camera.bin == 1:
                self.hardwarebin_checkbox.setChecked(True)
        else:
            self.hardwarebin_checkbox.setVisible(False)

    def set_camera(self, camera: Union[zwo.ZwoCamera, None]):
        self.camera = camera

    def set_temperature(self):
        self.camera.temperature = int(self.temperature_spinbox.cleanText())

    def set_red(self):
        self.camera.red_wb = int(self.red_spinbox.cleanText())

    def set_blue(self):
        self.camera.blue_wb = int(self.blue_spinbox.cleanText())

    def set_usb(self):
        self.camera.bandwidth = int(self.usb_spinbox.cleanText())
