import sys
from PySide6 import QtCore, QtWidgets
import zwoasi as asi
from equipment import zwo
from ui import ui_connectcamera

if sys.platform.startswith("win"):
    from equipment import ascom


class ConnectCamera(QtWidgets.QDialog, ui_connectcamera.Ui_ConnectCamera):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.size())

        self.result = None
        self.back_button = self.buttonbox.addButton("Back", QtWidgets.QDialogButtonBox.ResetRole)
        self.back_button.clicked.connect(self.back)
        self.back_button.setVisible(False)
        self.buttonbox.rejected.connect(self.cancel)
        self.ascom_commandlink.clicked.connect(self.connect_ascom)
        self.asi_commandlink.clicked.connect(self.select_asi)
        self.asi_connect_button.clicked.connect(self.connect_asi)
        self.refresh_asi_list()

    def refresh_asi_list(self):
        self.asi_combobox.clear()
        list_cam = asi.list_cameras()
        self.asi_combobox.addItems(list_cam)
        if len(list_cam) == 0:
            self.asi_connect_button.setDisabled(True)
            self.asi_combobox.setDisabled(True)
        else:
            self.asi_connect_button.setEnabled(True)
            self.asi_combobox.setEnabled(True)

    def select_asi(self):
        self.stackedWidget.setCurrentIndex(1)
        self.back_button.setVisible(True)
        self.back_button.setEnabled(True)

    def connect_asi(self):
        self.accept()

        asi_camera = self.asi_combobox.currentText()
        self.result = zwo.ZwoCamera(asi.list_cameras().index(asi_camera))

    def connect_ascom(self):
        self.accept()

        self.result = ascom.AscomCamera()

    def cancel(self):
        self.close()

    def back(self):
        self.stackedWidget.setCurrentIndex(0)
        self.back_button.setDisabled(True)
