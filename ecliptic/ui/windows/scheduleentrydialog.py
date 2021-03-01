from PySide6 import QtCore, QtWidgets
from ui.windows.uic.scheduleentry import Ui_ScheduleEntryDialog
from ui.frames.filter_settings import FilterSettingsFrame
from ui.delegates.widgets import *
import appglobals

class ScheduleEntryDialog(QtWidgets.QDialog, Ui_ScheduleEntryDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.table_frame = FilterSettingsFrame(parent=self)
        self.layout().insertWidget(0, self.table_frame)

        self.add_button.clicked.connect(self.table_frame.add_filter_row)
        self.remove_button.clicked.connect(self.table_frame.remove_filter_row)
    
    
