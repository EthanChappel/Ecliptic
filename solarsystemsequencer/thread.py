from PySide2 import QtCore
import numpy


class CameraThread(QtCore.QThread):
    exposure_done = QtCore.Signal(numpy.ndarray)

    def __init__(self, camera, widget, parent=None):
        super().__init__(parent)
        self.camera = camera
        self.parent = parent
        self.widget = widget

    def run(self):
        self.camera.video_mode = True

        while self.widget.isChecked():
            frame = self.camera.get_frame()
            self.exposure_done.emit(frame)

        self.camera.video_mode = False
