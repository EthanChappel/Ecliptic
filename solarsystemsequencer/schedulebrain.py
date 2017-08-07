from PyQt5 import QtCore, QtGui, QtWidgets
from ui import ui_schedulebrain


class ScheduleBrain(QtWidgets.QDialog, ui_schedulebrain.Ui_ScheduleBrainDialog):
    def __init__(self):
        super(ScheduleBrain, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.setFixedSize(self.size())
        self.exec_()