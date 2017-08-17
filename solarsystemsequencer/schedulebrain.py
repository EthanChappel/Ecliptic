import math
from typing import List
from PyQt5 import QtCore, QtWidgets
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

    def generate_schedule(self, targets: List[str], start: str="00:00", end: str="23:59",
                          max_sun_ele: int=-18, min_ele: int=12, max_ele: int=90, preference: str="Both"):
        time_range = list(pd.date_range(self.date+" "+start, self.date+" "+end, freq="60min").to_pydatetime())

        for r in reversed(time_range):
            compute = ComputeTargets(r, appglobals.location["Latitude"], appglobals.location["Longitude"])
            sun_alt = compute.object_alt("Sun")["alt"] * 180 / math.pi
            if sun_alt > max_sun_ele:
                time_range.remove(r)

            # Limit altitude of targets
            candidates = [t for t in targets if min_ele <= compute.object_alt(t)["alt"] * 180 / math.pi <= max_ele]

            # Stay on one side of meridian if set
            if preference == "East":
                candidates = [t for t in candidates if 0 <= compute.object_alt(t)["az"] * 180 / math.pi < 180]
            elif preference == "West":
                candidates = [t for t in candidates if 180 <= compute.object_alt(t)["az"] * 180 / math.pi < 360]

    def ok(self):
        self.generate_schedule(targets=[t.text() for t in self.targets_buttongroup.buttons() if t.isChecked()],
                               start=self.start_timeedit.text(), end=self.end_timeedit.text(),
                               max_sun_ele=int(self.sunelevation_spinbox.cleanText()),
                               preference=self.directional_combobox.currentText())
        self.accept()
