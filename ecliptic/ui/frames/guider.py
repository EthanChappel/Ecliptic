import os
import json
from PySide2 import QtWidgets
from .uic.uic_guider import Ui_GuiderFrame
import appglobals


class GuiderFrame(QtWidgets.QFrame, Ui_GuiderFrame):
    def __init__(self, parent):
        self.parent = parent
        
        super().__init__(self.parent)
        self.setupUi(self)


