import os
from PyQt5 import QtCore, QtGui, QtWidgets
import zwoasi as asi
import ui_connectcamera
import appglobals


class ConnectCamera(QtWidgets.QDialog, ui_connectcamera.Ui_ConnectCamera):
    def __init__(self):
        super(ConnectCamera, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.size())
        self.accepted = False
        self.asi_camera = None
        self.buttonbox.accepted.connect(self.ok)
        self.buttonbox.rejected.connect(self.cancel)
        self.refresh_asilist()
        self.asi_sync_button.clicked.connect(self.refresh_asilist)

    def refresh_asilist(self):
        self.asi_combobox.clear()
        list_cam = asi.list_cameras()
        self.asi_combobox.addItems(list_cam)
        if len(list_cam) == 0:
            self.asi_combobox.setDisabled(True)
            self.asi_radio.setDisabled(True)
            self.asi_label.setDisabled(True)
            self.asi_radio.setChecked(False)
        else:
            self.asi_combobox.setEnabled(True)
            self.asi_radio.setEnabled(True)
            self.asi_label.setEnabled(True)

    def ok(self):
        self.accepted = True
        self.asi_camera = self.asi_combobox.currentText()
        self.accept()

    def cancel(self):
        self.close()
