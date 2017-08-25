import math
import datetime
import json
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

    def generate_schedule(self, targets: List[str], start_time: str, end_time: str, max_sun_ele: int, min_ele: int,
                          max_ele: int, interval: int, preference: str, target_pref: str, no_target_action: str,
                          end_action: str):

        time_range = list(pd.date_range(self.date + " " + start_time, self.date + " " + end_time,
                                        freq=str(interval)+"min").to_pydatetime())

        schedule = {}
        for r in reversed(time_range):
            compute = ComputeTargets(r, appglobals.location["Latitude"], appglobals.location["Longitude"])
            sun_alt = compute.object_alt("Sun")["alt"] * 180 / math.pi
            if sun_alt > max_sun_ele:
                time_range.remove(r)

        for r in time_range:
            compute = ComputeTargets(r, appglobals.location["Latitude"], appglobals.location["Longitude"])
            # Limit altitude of targets
            candidates = [t for t in targets if min_ele <= compute.object_alt(t)["alt"] * 180 / math.pi <= max_ele]

            # Stay on one side of meridian if set
            if preference == "East":
                candidates = [t for t in candidates if 0 <= compute.object_alt(t)["az"] * 180 / math.pi < 180]
            elif preference == "West":
                candidates = [t for t in candidates if 180 <= compute.object_alt(t)["az"] * 180 / math.pi < 360]
            schedule[r] = candidates

        final = {}
        prev = None
        # TODO: Meridian flips
        for l in schedule:
            compute = ComputeTargets(l, appglobals.location["Latitude"], appglobals.location["Longitude"])
            target = None
            if target_pref == "Less for longer":
                lowest = max_ele
                for t in schedule.get(l):
                    if min_ele < compute.object_alt(t)["alt"] * 180 / math.pi < lowest:
                        pass
                        '''target = t
                        lowest = compute.object_alt(t)["alt"] * 180 / math.pi'''
            elif target_pref == "Prefer highest":
                highest = min_ele
                for t in schedule.get(l):
                    if max_ele > compute.object_alt(t)["alt"] * 180 / math.pi > highest:
                        target = t
                        highest = compute.object_alt(t)["alt"] * 180 / math.pi
                else:
                    if target is None and highest == min_ele:
                        target = no_target_action
            # Add to final if it wasn't previously added
            if target != prev:
                final[l] = target
                prev = target
        date = [int(i) for i in self.date.split("/")]
        time = [int(i) for i in end_time.split(":")]
        final[datetime.datetime(date[0], date[1], date[2], time[0], time[1])] = end_action
        appglobals.schedule[self.date] = [{"Target": final.get(t), "Time": str(t.time()), "Filter": "", "Exposure": "0",
                                           "Gain": "0", "Integration": "0"} for t in final]
        with open("schedule.json", "w") as f:
            json.dump(appglobals.schedule, f, indent=4)

    def ok(self):
        self.generate_schedule(targets=[t.text() for t in self.targets_buttongroup.buttons() if t.isChecked()],
                               start_time=self.start_timeedit.text(),
                               end_time=self.end_timeedit.time().toString(),
                               max_sun_ele=self.sunelevation_spinbox.value(),
                               min_ele=self.minelevation_spinbox.value(),
                               max_ele=self.maxelevation_spinbox.value(),
                               interval=self.interval_spinbox.value(),
                               preference=self.directional_combobox.currentText(),
                               target_pref=self.targetpreference_combobox.currentText(),
                               no_target_action=self.notarget_combobox.currentText(),
                               end_action=self.endaction_combobox.currentText())
        self.accept()
