from PySide2 import QtCore, QtGui
from PIL import Image, ImageQt
from equipment.ascom import AscomTelescope


class TelescopeThread(QtCore.QThread):
    setup_complete = QtCore.Signal(AscomTelescope)
    setup_failed = QtCore.Signal(Exception)

    def __init__(self, telescope, parent=None):
        super().__init__(parent)
        self.telescope = telescope
        self.parent = parent
    
    def run(self):
        try:
            telescope = AscomTelescope()
            self.setup_complete.emit(telescope)
        except Exception as e:
            self.setup_failed.emit(e)

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
