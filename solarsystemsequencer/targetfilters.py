from PyQt5 import QtCore, QtGui, QtWidgets
from ui import ui_targetfilters


class TargetFilters(QtWidgets.QDialog, ui_targetfilters.Ui_TargetFilters):
    def __init__(self):
        # TODO: Make dialog function!
        super(TargetFilters, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.size())
        self.exec_()
