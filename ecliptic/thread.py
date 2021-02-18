from PySide6 import QtCore, QtGui
from formats.ser3 import Ser3Writer
from PIL import Image, ImageQt
from astropy.coordinates import get_body
from astropy.coordinates import Angle
from astropy.time import Time
import astropy.units as u
from equipment.ascom import AscomTelescope


class TelescopeConnectThread(QtCore.QThread):
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


class TelescopeSlewThread(QtCore.QThread):
    slew_complete = QtCore.Signal()

    def __init__(self, telescope, target, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.telescope = telescope
        self.target = target
    
    def run(self):
        if self.target == "Home":
            self.telescope.goto_home()
        elif self.target == "Stop":
            self.telescope.tracking = False
        else:
            body = get_body(self.target.lower(), Time.now())
            self.telescope.goto(body.ra.hour, body.dec.degree)


class CameraThread(QtCore.QThread):
    exposure_done = QtCore.Signal(object)
    setup_complete = QtCore.Signal(object)

    def __init__(self, camera, widget, parent=None):
        super().__init__(parent)
        self.camera = camera
        self.parent = parent
        self.widget = widget
        self.writer = None

        if self.parent:
            self.parent.start_recording.connect(self.set_writer)
            self.parent.stop_recording.connect(self.set_writer)

    def run(self):
        self.camera.video_mode = True

        while self.widget.isChecked():
            frame = self.camera.get_frame()
            if self.writer:
                self.writer.add_frame(frame.tobytes())
            image = Image.fromarray(frame)
            self.exposure_done.emit(image)

        self.camera.video_mode = False
    
    @QtCore.Slot()
    def set_writer(self, writer=None):
        if type(writer) is None:
            self.writer.close()

        self.writer = writer

class FinderCameraThread(CameraThread):
    def run(self):
        self.camera.video_mode = True
        frame = self.camera.get_frame()
        self.camera.video_mode = False
        image = Image.fromarray(frame)
        self.exposure_done.emit(image)


class PlateSolveThread(QtCore.QThread):
    plate_solve_complete = QtCore.Signal(object)

    def __init__(self, solver, image, ra_h=None, dec_d=None, radius_d=None, fov_d=None, down_sample=None, debug=False, parent=None):
        super().__init__(parent)

        self.solver = solver
        self.image = image
        self.ra = ra_h
        self.dec = dec_d
        self.radius = radius_d
        self.fov = fov_d
        self.down_sample = down_sample
        self.debug = debug
    
    def run(self):
        self.plate_solve_complete.emit(
            self.solver.solve(self.image, self.ra, self.dec, self.radius, self.fov, self.down_sample, self.debug)
        )

class GotoAndVerifyThread(QtCore.QThread):
    exposure_done = QtCore.Signal(object)
    plate_solve_complete = QtCore.Signal(object)
    plate_solve_failed = QtCore.Signal(object)

    def __init__(self, target, accuracy, max_attempts, telescope, finder, solver, radius_d=None, fov_d=None, down_sample=None, debug=False, parent=None):
        super().__init__(parent)
        
        self.target = target
        self.accuracy = Angle(accuracy * u.arcsec)
        self.attempts = max_attempts
        self.telescope = telescope
        self.finder = finder
        self.solver = solver
        self.radius = radius_d
        self.fov = fov_d
        self.down_sample = down_sample
        self.debug = debug
        self.parent = parent

    # TODO: Utilize other threads.
    def run(self):
        results = None
        separation = Angle(180 * u.deg)
        
        # Repeat until slew is sufficiently accurate or max attempts reached.
        while separation > self.accuracy and self.attempts > 0:
            self.telescope.goto(self.target.ra.hour, self.target.dec.degree)

            # Capture image from finder.
            self.finder.video_mode = True
            frame = self.finder.get_frame()
            self.finder.video_mode = False
            image = Image.fromarray(frame)
            self.exposure_done.emit(image)

            try:
                # Get real position of telescope.
                results = self.solver.solve(
                    image,
                    self.target.ra.hour,
                    self.target.dec.deg,
                    self.radius,
                    self.fov,
                    self.down_sample,
                    self.debug,
                )
                self.plate_solve_complete.emit(results)
            except FileNotFoundError:
                plate_solve_failed.emit(FileNotFoundError)
                return

            self.telescope.sync(results.ra.hour, results.dec.deg)

            # Calculate accuracy of slew.
            separation = results.separation(self.target)
            self.attempts -= 1
