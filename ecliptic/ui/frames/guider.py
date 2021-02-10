from PySide6 import QtGui, QtWidgets
from PIL import ImageQt
from .uic.uic_guider import Ui_GuiderFrame
from astrometry.astap import AstapSolver
import appglobals


class GuiderFrame(QtWidgets.QFrame, Ui_GuiderFrame):
    def __init__(self, parent):
        self.parent = parent
        self.solver = None
        self.image = None
        
        super().__init__(self.parent)
        self.setupUi(self)

        self.plate_solve_button.clicked.connect(self.plate_solve)
        self.set_solver(AstapSolver(appglobals.settings['ASTAP Location']))

    def preview(self, image):
        self.image = image
        pixmap = ImageQt.toqpixmap(self.image)
        self.guider_preview_label.setPixmap(pixmap)
    
    def set_solver(self, solver):
        self.solver = solver
    
    def plate_solve(self):
        self.solver.solve(self.image)

