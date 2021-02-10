from PySide6 import QtGui, QtWidgets
from PIL import ImageQt
from .uic.uic_guider import Ui_GuiderFrame


class GuiderFrame(QtWidgets.QFrame, Ui_GuiderFrame):
    def __init__(self, parent):
        self.parent = parent
        self.image = None
        
        super().__init__(self.parent)
        self.setupUi(self)

    def preview(self, image):
        self.image = image
        pixmap = ImageQt.toqpixmap(self.image)
        self.guider_preview_label.setPixmap(pixmap)
