from PySide2 import QtWidgets
from ui import ui_guiderparameters


class GuiderParameters(QtWidgets.QFrame, ui_guiderparameters.Ui_GuiderParameters):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # TODO: Implement!
