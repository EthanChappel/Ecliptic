import ephem
import numpy as np
from scipy.interpolate import spline
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from cycler import cycler
from ui_targetswindow import Ui_Dialog
import computetargets
import appglobals


class TargetsDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(TargetsDialog, self).__init__()

        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.schedule_figure = Figure()
        self.sched_plot = self.schedule_figure.add_subplot(1, 1, 1, axisbg="black")
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

    def generate(self, latitude, longitude):
        """Generate graph whenever date is changed."""
        self.sched_plot.lines = []
        self.sched_plot.patches = []
        for t in appglobals.targets_tuple:
            alt_list = []
            hour_list = []
            for h in range(-1, 26):
                timestr = (str(self.schedule_dateedit.text()) + " " + str(h) + ":00:00")
                alt = self.compute_target(t, timestr, latitude, longitude)

                alt_split = str(ephem.degrees(alt["alt"]))
                alt_split = alt_split.split(":")
                alt_decimal = int(alt_split[0]) + (int(alt_split[1]) / 60) + (float(alt_split[2]) / 3600)
                alt_list.append(alt_decimal)
                hour_list.append(h)
            alt_array = np.array(alt_list)
            hour_array = np.array(hour_list)
            x_smooth = np.linspace(hour_array.min(), alt_array.max(), 250)
            y_smooth = spline(hour_array, alt_array, x_smooth)
            self.sched_plot.plot(x_smooth, y_smooth, gid=t)
        twilight = self.compute_twilight(latitude, longitude)

        try:
            sun_rise = twilight[0][3] + (twilight[0][4] / 60) + (twilight[0][5] / 3600)
            sun_set = twilight[4][3] + (twilight[4][4] / 60) + (twilight[4][5] / 3600)
        except TypeError:
            sun_rise = None
            sun_set = None

        """
        try:
            civil_rise = twilight[1][3]+(twilight[1][4]/60)+(twilight[1][5]/3600)
            civil_set = twilight[5][3] + (twilight[5][4] / 60) + (twilight[5][5] / 3600)
        except TypeError:
            civil_rise = None
            civil_set = None

        try:
            nautical_rise = twilight[2][3] + (twilight[2][4] / 60) + (twilight[2][5] / 3600)
            nautical_set = twilight[6][3] + (twilight[6][4] / 60) + (twilight[6][5] / 3600)
        except TypeError:
            nautical_rise = None
            nautical_set = None

        try:
            astronomical_rise = twilight[3][3] + (twilight[3][4] / 60) + (twilight[3][5] / 3600)
            astronomical_set = twilight[7][3] + (twilight[7][4] / 60) + (twilight[7][5] / 3600)
        except TypeError:
            astronomical_rise = None
            astronomical_set = None

        # All statements with + 24 or - 24 are slightly inaccurate.
        try:
            if astronomical_rise > nautical_rise:
                self.sched_plot.axvspan(astronomical_rise - 24, nautical_rise, color="blue", alpha=0.15)
                self.sched_plot.axvspan(astronomical_rise, nautical_rise + 24, color="blue", alpha=0.15)
                print(astronomical_rise, astronomical_set, twilight[11])
            else:
                self.sched_plot.axvspan(astronomical_rise - 24, nautical_rise - 24, color="blue", alpha=0.15)
                self.sched_plot.axvspan(astronomical_rise, nautical_rise, color="blue", alpha=0.15)
                print(astronomical_rise, astronomical_set, twilight[11])
        except TypeError:
            try:
                self.sched_plot.axvspan(astronomical_rise - 24, astronomical_set - 24, color="blue", alpha=0.15)
                self.sched_plot.axvspan(astronomical_rise, astronomical_set, color="blue", alpha=0.15)
                print(astronomical_rise, astronomical_set, twilight[11])
            except TypeError:
                if nautical_set > nautical_rise:
                    self.sched_plot.axvspan(nautical_set - 24, nautical_rise, color="blue", alpha=0.15)
                    self.sched_plot.axvspan(nautical_set, nautical_rise + 24, color="blue", alpha=0.15)
                else:
                    self.sched_plot.axvspan(nautical_set, nautical_rise - 24, color="blue", alpha=0.15)
                    self.sched_plot.axvspan(nautical_set + 24, nautical_rise, color="blue", alpha=0.15)
                print(astronomical_rise, astronomical_set, twilight[11])

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
        """
        try:
            if sun_rise > sun_set:
                self.sched_plot.axvspan(sun_rise - 24, sun_set, color="yellow", alpha=0.25)
                self.sched_plot.axvspan(sun_rise, sun_set + 24, color="yellow", alpha=0.25)
            else:
                self.sched_plot.axvspan(sun_rise, sun_set, color="yellow", alpha=0.25)
                self.sched_plot.axvspan(sun_rise - 24, sun_set-24, color="yellow", alpha=0.25)
        except TypeError:
            if "above" in str(twilight[8]):
                self.sched_plot.axvspan(0, 24, color="yellow", alpha=0.25)
        """
        try:
            if sun_set > civil_set:
                self.sched_plot.axvspan(sun_set - 24, civil_set, color="orange", alpha=0.25)
                self.sched_plot.axvspan(sun_set, civil_set + 24, color="orange", alpha=0.25)
            else:
                self.sched_plot.axvspan(sun_set, civil_set, color="orange", alpha=0.25)
                self.sched_plot.axvspan(sun_set - 24, civil_set - 24, color="orange", alpha=0.25)
        except TypeError:
            try:
                self.sched_plot.axvspan(civil_rise - 24, civil_set - 24, color="orange", alpha=0.25)
                self.sched_plot.axvspan(civil_rise, civil_set, color="orange", alpha=0.25)
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
            pass

        try:
            if nautical_set > astronomical_set:
                self.sched_plot.axvspan(nautical_set - 24, astronomical_set, color="blue", alpha=0.15)
                self.sched_plot.axvspan(nautical_set, astronomical_set + 24, color="blue", alpha=0.15)
            else:
                self.sched_plot.axvspan(nautical_set, astronomical_set, color="blue", alpha=0.15)
                self.sched_plot.axvspan(nautical_set - 24, astronomical_set - 24, color="blue", alpha=0.15)
        except TypeError:
            pass
        """
        self.canvas.draw()

    @staticmethod
    def compute_target(target, time, latitude, longitude, print_=False):
        compute_alt = computetargets.ComputeTargets(time, latitude, longitude)
        alt = compute_alt.object_alt(target)
        if print_:
            print("Target: %-5s, Time: %-19s, RA: %-11s, Dec°: %-11s, Az: %-11s, Alt°: %-11s"
                  % (target, str(time), str(ephem.hours(alt["ra"])), str(ephem.degrees(alt["dec"])),
                     str(ephem.degrees(alt["az"])), str(ephem.degrees(alt["alt"]))))
        return alt

    def compute_twilight(self, latitude, longitude, print_=False):
        time = str(self.schedule_dateedit.text()) + " 12:00"
        twi = computetargets.ComputeTargets(time, latitude, longitude)
        alt = twi.twilight()
        if print_:
            print(alt)
        return alt

    def on_plot_hover(self, event):
        """Show QToolTip when line is hovered over in graph."""
        for curve in self.sched_plot.get_lines():
            if curve.contains(event)[0]:
                QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), curve.get_gid())
