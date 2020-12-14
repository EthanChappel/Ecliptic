from PySide6 import QtCore, QtWidgets
from ui.ui_scheduleentry import Ui_ScheduleEntryDialog

class ScheduleEntryDialog(QtWidgets.QDialog, Ui_ScheduleEntryDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)