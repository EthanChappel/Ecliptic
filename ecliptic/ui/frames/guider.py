from PySide2 import QtGui, QtWidgets
from .uic.uic_guider import Ui_GuiderFrame


class GuiderFrame(QtWidgets.QFrame, Ui_GuiderFrame):
    def __init__(self, parent):
        self.parent = parent
        
        super().__init__(self.parent)
        self.setupUi(self)

    def preview(self, frame: QtGui.QPixmap):
        self.guider_preview_label.setPixmap(frame)
