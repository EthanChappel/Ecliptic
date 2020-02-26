from PySide2 import QtCore, QtGui
from PIL import Image, ImageQt


class CameraThread(QtCore.QThread):
    exposure_done = QtCore.Signal(QtGui.QPixmap)

    def __init__(self, camera, widget, parent=None):
        super().__init__(parent)
        self.camera = camera
        self.parent = parent
        self.widget = widget

    def run(self):
        self.camera.video_mode = True

        while self.widget.isChecked():
            frame = self.camera.get_frame()
            image = Image.fromarray(frame)
            pix = ImageQt.toqpixmap(image)
            self.exposure_done.emit(pix)

        self.camera.video_mode = False
