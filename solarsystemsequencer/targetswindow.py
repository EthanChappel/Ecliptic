from datetime import timedelta
from typing import List
import ephem
import numpy as np
from scipy.interpolate import spline
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from cycler import cycler
from ui.ui_targetswindow import Ui_Dialog
import computetargets
from conversions import time
import appglobals


class TargetsDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(TargetsDialog, self).__init__()

        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.schedule_figure = Figure(facecolor=(0.333, 0.333, 0.333))
        self.sched_plot = self.schedule_figure.add_subplot(1, 1, 1, facecolor="black")
        self.sched_plot.spines["bottom"].set_color("white")
        self.sched_plot.spines["top"].set_color("white")
        self.sched_plot.spines["right"].set_color("white")
        self.sched_plot.spines["left"].set_color("white")
        self.sched_plot.tick_params(axis="x", colors="white", which="both")
        self.sched_plot.tick_params(axis="y", colors="white", which="both")
        self.sched_plot.set_prop_cycle(cycler("color", ["gray", "white", "red", "orange", "tan", "aqua", "blue"]))
        self.sched_plot.set_ylim([0, 90])
        self.sched_plot.set_xlim([0, 24])
        self.sched_plot.set_xticks(np.arange(0, 25, 6))
        self.sched_plot.set_xticks(np.arange(0, 25, 1), minor=True)
        self.sched_plot.set_yticks(np.arange(0, 91, 30))
        self.sched_plot.set_yticks(np.arange(0, 91, 10), minor=True)
        self.sched_plot.grid(which="both", color="gray")
        self.setup_gui()
        self.schedule_figure.tight_layout()
        self.canvas.mpl_connect("motion_notify_event", self.on_plot_hover)
        self.generate(appglobals.location["Latitude"], appglobals.location["Longitude"])

    def setup_gui(self):
        self.set_today()
        self.canvas = FigureCanvas(self.schedule_figure)
        self.verticalLayout_2.addWidget(self.canvas)
        self.schedule_dateedit.dateChanged.connect(
            lambda: self.generate(appglobals.location["Latitude"], appglobals.location["Longitude"]))
        self.today_btn.clicked.connect(self.set_today)

    def set_today(self):
        """Set graph date to current date."""
        self.schedule_dateedit.setDateTime(QtCore.QDateTime.currentDateTime())

    def generate(self, latitude: List[int]=None, longitude: List[int]=None):
        """Generate graph whenever date is changed."""
        if latitude is None:
            latitude = appglobals.location["Latitude"]
        if longitude is None:
            longitude = appglobals.location["Longitude"]
        dtime = self.schedule_dateedit.dateTime().toPyDateTime()
        dtime = dtime.replace(hour=0, minute=0, second=0, microsecond=0)
        self.sched_plot.lines = []
        self.sched_plot.patches = []
        for t in appglobals.targets_tuple:
            alt_list = []
            hour_list = []
            for h in range(-1, 26):
                time_h = dtime + timedelta(hours=h)
                alt = computetargets.get_alt(t, time_h, latitude, longitude)

                alt_split = str(ephem.degrees(alt)).split(":")
                alt_decimal = int(alt_split[0]) + (int(alt_split[1]) / 60) + (float(alt_split[2]) / 3600)
                alt_list.append(alt_decimal)
                hour_list.append(h)
            alt_array = np.array(alt_list)
            hour_array = np.array(hour_list)
            x_smooth = np.linspace(hour_array.min(), alt_array.max(), 250)
            y_smooth = spline(hour_array, alt_array, x_smooth)
            self.sched_plot.plot(x_smooth, y_smooth, gid=t)

        day_sun_rise = computetargets.previous_rise("Sun", dtime, 0, latitude, longitude)
        day_sun_set = computetargets.next_set("Sun", dtime, 0, latitude, longitude)
        try:
            rise_time = day_sun_rise.datetime()
            set_time = day_sun_set.datetime()
            sun_rise = time.get_decimal(rise_time.hour, rise_time.minute, rise_time.second)
            sun_set = time.get_decimal(set_time.hour, set_time.minute, set_time.second)
        except AttributeError:
            sun_rise = None
            sun_set = None

        civil_sun_rise = computetargets.previous_rise("Sun", dtime, -6, latitude, longitude)
        civil_sun_set = computetargets.next_set("Sun", dtime, -6, latitude, longitude)
        try:
            rise_time = civil_sun_rise.datetime()
            set_time = civil_sun_set.datetime()
            civil_rise = time.get_decimal(rise_time.hour, rise_time.minute, rise_time.second)
            civil_set = time.get_decimal(set_time.hour, set_time.minute, set_time.second)
        except AttributeError:
            civil_rise = None
            civil_set = None

        nautical_sun_rise = computetargets.previous_rise("Sun", dtime, -12, latitude, longitude)
        nautical_sun_set = computetargets.next_set("Sun", dtime, -12, latitude, longitude)
        try:
            rise_time = nautical_sun_rise.datetime()
            nautical_rise = time.get_decimal(rise_time.hour, rise_time.minute, rise_time.second)
            set_time = nautical_sun_set.datetime()
            nautical_set = time.get_decimal(set_time.hour, set_time.minute, set_time.second)
        except AttributeError:
            nautical_rise = None
            nautical_set = None

        astronomical_sun_rise = computetargets.previous_rise("Sun", dtime, -18, latitude, longitude)
        astronomical_sun_set = computetargets.next_set("Sun", dtime, -18, latitude, longitude)
        try:
            rise_time = astronomical_sun_rise.datetime()
            astronomical_rise = time.get_decimal(rise_time.hour, rise_time.minute, rise_time.second)
            set_time = astronomical_sun_set.datetime()
            astronomical_set = time.get_decimal(set_time.hour, set_time.minute, set_time.second)
        except AttributeError:
            astronomical_rise = None
            astronomical_set = None

        # FIXME: Shades can act weird when location is set to high latitudes
        try:
            if astronomical_rise > nautical_rise:
                self.sched_plot.axvspan(astronomical_rise - 24, nautical_rise, color="blue", alpha=0.15)
                self.sched_plot.axvspan(astronomical_rise, nautical_rise + 24, color="blue", alpha=0.15)
            else:
                self.sched_plot.axvspan(astronomical_rise - 24, nautical_rise - 24, color="blue", alpha=0.15)
                self.sched_plot.axvspan(astronomical_rise, nautical_rise, color="blue", alpha=0.15)
        except TypeError:
            try:
                self.sched_plot.axvspan(astronomical_rise - 24, astronomical_set - 24, color="blue", alpha=0.15)
                self.sched_plot.axvspan(astronomical_rise, astronomical_set, color="blue", alpha=0.15)
            except TypeError:
                pass

        try:
            if civil_rise < nautical_rise:
                self.sched_plot.axvspan(nautical_rise - 24, civil_rise, color="purple", alpha=0.25)
                self.sched_plot.axvspan(nautical_rise, civil_rise + 24, color="purple", alpha=0.25)
            else:
                self.sched_plot.axvspan(nautical_rise - 24, civil_rise - 24, color="purple", alpha=0.3)
                self.sched_plot.axvspan(nautical_rise, civil_rise, color="purple", alpha=0.3)
        except TypeError:
            try:
                self.sched_plot.axvspan(nautical_rise - 24, nautical_set - 24, color="purple", alpha=0.25)
                self.sched_plot.axvspan(nautical_rise, nautical_set, color="purple", alpha=0.25)
            except TypeError:
                pass

        try:
            if sun_rise < civil_rise:
                self.sched_plot.axvspan(civil_rise - 24, sun_rise, color="orange", alpha=0.25)
                self.sched_plot.axvspan(civil_rise, sun_rise + 24, color="orange", alpha=0.25)
            else:
                self.sched_plot.axvspan(civil_rise - 24, sun_rise - 24, color="orange", alpha=0.25)
                self.sched_plot.axvspan(civil_rise, sun_rise, color="orange", alpha=0.25)
        except TypeError:
            try:
                self.sched_plot.axvspan(civil_rise - 24, civil_set - 24, color="orange", alpha=0.25)
                self.sched_plot.axvspan(civil_rise, civil_set, color="orange", alpha=0.25)
            except TypeError:
                pass

        try:
            if sun_rise > sun_set:
                self.sched_plot.axvspan(sun_rise - 24, sun_set, color="yellow", alpha=0.25)
                self.sched_plot.axvspan(sun_rise, sun_set + 24, color="yellow", alpha=0.25)
            else:
                self.sched_plot.axvspan(sun_rise, sun_set, color="yellow", alpha=0.25)
                self.sched_plot.axvspan(sun_rise - 24, sun_set-24, color="yellow", alpha=0.25)
        except TypeError:
            if isinstance(day_sun_rise, ephem.AlwaysUpError) and isinstance(day_sun_set, ephem.AlwaysUpError):
                self.sched_plot.axvspan(0, 24, color="yellow", alpha=0.25)

        try:
            if sun_set > civil_set:
                self.sched_plot.axvspan(sun_set - 24, civil_set, color="orange", alpha=0.25)
                self.sched_plot.axvspan(sun_set, civil_set + 24, color="orange", alpha=0.25)
            else:
                self.sched_plot.axvspan(sun_set, civil_set, color="orange", alpha=0.25)
                self.sched_plot.axvspan(sun_set - 24, civil_set - 24, color="orange", alpha=0.25)
        except TypeError:
            try:
                self.sched_plot.axvspan(sun_set - 24, sun_rise - 24, color="orange", alpha=0.25)
                self.sched_plot.axvspan(sun_set, sun_rise, color="orange", alpha=0.25)
            except TypeError:
                pass

        try:
            if civil_set > nautical_set:
                self.sched_plot.axvspan(civil_set - 24, nautical_set, color="purple", alpha=0.3)
                self.sched_plot.axvspan(civil_set, nautical_set + 24, color="purple", alpha=0.3)
            else:
                self.sched_plot.axvspan(civil_set, nautical_set, color="purple", alpha=0.3)
                self.sched_plot.axvspan(civil_set - 24, nautical_set - 24, color="purple", alpha=0.3)
        except TypeError:
            try:
                self.sched_plot.axvspan(civil_set, civil_rise, color="purple", alpha=0.3)
                self.sched_plot.axvspan(civil_set - 24, civil_rise - 24, color="purple", alpha=0.3)
            except TypeError:
                pass

        try:
            if nautical_set > astronomical_set:
                self.sched_plot.axvspan(nautical_set - 24, astronomical_set, color="blue", alpha=0.15)
                self.sched_plot.axvspan(nautical_set, astronomical_set + 24, color="blue", alpha=0.15)
            else:
                self.sched_plot.axvspan(nautical_set, astronomical_set, color="blue", alpha=0.15)
                self.sched_plot.axvspan(nautical_set - 24, astronomical_set - 24, color="blue", alpha=0.15)
        except TypeError:
            try:
                self.sched_plot.axvspan(nautical_set, nautical_rise, color="blue", alpha=0.15)
                self.sched_plot.axvspan(nautical_set - 24, nautical_rise - 24, color="blue", alpha=0.15)
            except TypeError:
                pass

        self.canvas.draw()

    def on_plot_hover(self, event):
        """Show QToolTip when line is hovered over in graph."""
        for curve in self.sched_plot.get_lines():
            if curve.contains(event)[0]:
                QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), curve.get_gid())
