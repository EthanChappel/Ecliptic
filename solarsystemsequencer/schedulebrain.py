from PyQt5 import QtCore, QtWidgets
from ui import ui_schedulebrain
from brains import sched_brain


class ScheduleBrain(QtWidgets.QDialog, ui_schedulebrain.Ui_ScheduleBrainDialog):
    def __init__(self, date):
        super(ScheduleBrain, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.size())
        self.buttonbox.accepted.connect(self.ok)
        self.date = date
        self.exec_()

    def ok(self):
        sched_brain.generate(targets=[t.text() for t in self.targets_buttongroup.buttons() if t.isChecked()],
                             date=self.date,
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
