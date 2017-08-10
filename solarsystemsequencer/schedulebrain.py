from typing import Tuple
from PyQt5 import QtCore, QtWidgets
import pandas as pd
from ui import ui_schedulebrain


class ScheduleBrain(QtWidgets.QDialog, ui_schedulebrain.Ui_ScheduleBrainDialog):
    def __init__(self, date):
        super(ScheduleBrain, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.size())
        self.buttonbox.accepted.connect(self.ok)
        self.date = date
        self.exec_()

    def generate_schedule(self, twilight=None, time: Tuple[str, str]=None, elevation=None, preference=None):
        if time is not None:
            time_range = pd.date_range(self.date+" "+time[0], self.date+" "+time[1], freq="5min").to_pydatetime()
        if twilight is not None:
            pass
        if elevation is not None:
            pass
        if preference is not None:
            pass

    def ok(self):
        self.generate_schedule(time=(self.start_timeedit.text(), self.end_timeedit.text()))
        self.accept()
