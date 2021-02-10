from PySide6 import QtGui, QtWidgets
from PIL import ImageQt
from .uic.uic_camera import Ui_CameraFrame


class CameraFrame(QtWidgets.QFrame, Ui_CameraFrame):
    def __init__(self, parent):
        self.parent = parent
        
        super().__init__(self.parent)
        self.setupUi(self)
    
    def preview(self, image):
        pixmap = ImageQt.toqpixmap(image)
        self.camera_preview_label.setPixmap(pixmap)
