import math
from typing import Tuple
from PyQt5 import QtCore, QtWidgets
import ephem
import pandas as pd
import appglobals
from computetargets import ComputeTargets
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

    def generate_schedule(self, start: str="00:00", end: str="23:59", max_sun_ele: int=-18, elevation=None,
                          preference=None):
        time_range = list(pd.date_range(self.date+" "+start, self.date+" "+end, freq="60min").to_pydatetime())

        for t in reversed(time_range):
            targets = ComputeTargets(t, appglobals.location["Latitude"], appglobals.location["Longitude"])
            sun_alt = targets.object_alt("Sun")["alt"] * 180 / math.pi
            if sun_alt > max_sun_ele:
                time_range.remove(t)

        if elevation is not None:
            pass

        if preference is not None:
            pass

    def ok(self):
        self.generate_schedule(start=self.start_timeedit.text(), end=self.end_timeedit.text(),
                               max_sun_ele=int(self.sunelevation_spinbox.cleanText()))
        self.accept()
