from PySide6.QtWidgets import QDialog
from ui.ui_scheduleentry import Ui_ScheduleEntryDialog

class ScheduleEntryDialog(QDialog, Ui_ScheduleEntryDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)