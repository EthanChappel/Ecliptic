import sqlite3
from PySide6 import QtCore, QtGui, QtWidgets
from .uic.uic_schedule import Ui_ScheduleFrame
from ..delegates.widgets import *
from ..delegates.custom import *
from scheduleentrydialog import ScheduleEntryDialog
import appglobals
from database import Database


class ScheduleFrame(QtWidgets.QFrame, Ui_ScheduleFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        self.setupUi(self)

        self.database = Database('database.sqlite3')

        self.max_schedule_id = self.database.schedule_max_id()

        self.row_count = self.schedule_table.rowCount()

        # Create Delegates for columns in schedule table.
        self.date_delegate = QDateTimeEditItemDelegate(self)
        self.target_delegate = QComboBoxItemDelegate(self, self.parent.target_list_model)
        self.parameters_delegate = QWindowEditorDelegate(ScheduleEntryDialog, self)

        self.schedule_table.hideColumn(0)

        # Connect functions to addrow_button and removerow_button
        self.addrow_button.clicked.connect(self.add_schedule_row)
        self.removerow_button.clicked.connect(self.remove_schedule_row)

        self.schedule_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        # Set item delegates for columns in schedule table.
        self.schedule_table.setItemDelegateForColumn(1, self.date_delegate)
        self.schedule_table.setItemDelegateForColumn(2, self.target_delegate)
        self.schedule_table.setItemDelegateForColumn(3, self.parameters_delegate)

        # Save whenever cell is changed.
        self.schedule_table.itemChanged.connect(self.save_schedule)

        self.load_schedule()

    def add_schedule_row(self):
        """Add row in schedule_table."""
        self.row_count = self.schedule_table.rowCount()
        self.schedule_table.insertRow(self.row_count)
        self.schedule_table.blockSignals(True)
        self.schedule_table.setItem(
            self.schedule_table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(self.max_schedule_id), QtCore.Qt.DisplayRole)
        )
        for i in range(1, self.schedule_table.columnCount()):
            if self.schedule_table.item(self.row_count, i) is None:
                self.schedule_table.setItem(self.row_count, i, QtWidgets.QTableWidgetItem())
        self.schedule_table.blockSignals(False)
        self.max_schedule_id += 1

    def remove_schedule_row(self):
        """Remove selected rows from schedule_table."""
        selected = self.schedule_table.selectedItems()
        rows = sorted({i.row() for i in selected}, reverse=True)
        for r in rows:
            row_id = int(self.schedule_table.item(r, 0).text())
            self.database.remove_schedule(row_id)
            self.schedule_table.removeRow(r)

    def save_schedule(self, item):
        """Save contents of schedule_table into schedule.json."""
        row = item.row()
        item = self.schedule_table.item
        self.schedule_table.blockSignals(True)
        try:
            b = QtGui.QBrush(QtCore.Qt.NoBrush)
            self.database.insert_or_update_schedule(
                int(self.schedule_table.item(row, 0).text()),
                self.schedule_table.item(row, 1).text(),
                self.schedule_table.item(row, 2).text(),
                self.schedule_table.item(row, 3).text(),
            )
            for i in range(self.schedule_table.columnCount()):
                self.schedule_table.item(row, i).setBackground(b)
        except sqlite3.IntegrityError:
            b = QtGui.QBrush(QtCore.Qt.SolidPattern)
            b.setColor(QtGui.QColor(150, 60, 60))
            for i in range(self.schedule_table.columnCount()):
                if self.schedule_table.item(row, i) is None:
                    self.schedule_table.setItem(row, i, QtWidgets.QTableWidgetItem())
                self.schedule_table.item(row, i).setBackground(b)
        finally:
            self.schedule_table.blockSignals(False)

    def load_schedule(self):
        """Load contents of schedule.json into schedule_table."""
        i = 0
        for r in self.database.cursor.execute('SELECT * FROM schedule ORDER BY start'):
            self.schedule_table.insertRow(i)
            self.schedule_table.blockSignals(True)
            self.schedule_table.setItem(
                i, 0,
                QtWidgets.QTableWidgetItem(str(r[0]), QtCore.Qt.DisplayRole)
            )
            self.schedule_table.setItem(
                i, 1,
                QtWidgets.QTableWidgetItem(r[1], QtCore.Qt.DisplayRole)
            )
            self.schedule_table.setItem(
                i, 2,
                QtWidgets.QTableWidgetItem(r[2], QtCore.Qt.DisplayRole)
            )
            self.schedule_table.setItem(
                i, 3,
                QtWidgets.QTableWidgetItem(r[3], QtCore.Qt.DisplayRole)
            )
            self.schedule_table.blockSignals(False)
            self.max_schedule_id += 1
            i += 1