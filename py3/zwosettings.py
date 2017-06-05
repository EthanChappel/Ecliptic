from PyQt5 import QtCore, QtGui, QtWidgets
import ui_zwosettings


class ZWOSettings(QtWidgets.QFrame, ui_zwosettings.Ui_ZWOSettings):
    def __init__(self):
        super(ZWOSettings, self).__init__()
        self.setupUi(self)