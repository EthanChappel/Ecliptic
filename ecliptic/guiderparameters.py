from PySide6 import QtWidgets
from ui.windows.uic.uic_guiderparameters import Ui_GuiderParameters


class GuiderParameters(QtWidgets.QFrame, Ui_GuiderParameters):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # TODO: Implement!
