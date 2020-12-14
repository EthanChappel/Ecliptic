from PySide6 import QtCore, QtWidgets
from ui.ui_scheduleentry import Ui_ScheduleEntryDialog

class ScheduleEntryDialog(QtWidgets.QDialog, Ui_ScheduleEntryDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.filter_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.add_filter_button.clicked.connect(self.add_filter_row)
        self.remove_filter_button.clicked.connect(self.remove_filter_row)

    def add_filter_row(self):
        """Add row in filter_table."""
        self.row_count = self.filter_table.rowCount()
        self.filter_table.insertRow(self.row_count)

    def remove_filter_row(self):
        """Remove selected rows from filter_table."""
        for model_index in self.filter_table.selectionModel().selection().indexes():
            index = QtCore.QPersistentModelIndex(model_index)
            self.filter_table.removeRow(index.row())
