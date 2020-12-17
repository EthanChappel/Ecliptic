import os
import json
from typing import List, Dict
from PySide2 import QtCore, QtWidgets
from .uic.uic_filters import Ui_FiltersFrame
from ..delegates.widgets import *
import appglobals


class FiltersFrame(QtWidgets.QFrame, Ui_FiltersFrame):
    filters_changed = QtCore.Signal()

    def __init__(self, parent):
        self.parent = parent
        
        super().__init__(self.parent)
        self.setupUi(self)

        self.filters_changed.connect(self.parent.update_filters)

        self.add_button.clicked.connect(self.add_filter_row)
        self.remove_button.clicked.connect(self.remove_filter_row)

        self.load_filters(appglobals.filters)

        self.filter_list_model = QtCore.QStringListModel()

        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Create Delegates for columns in filters table.
        self.position_delegate = QSpinBoxItemDelegate(self)
        self.lower_cutoff_delegate = QSpinBoxItemDelegate(self, 0, 2000, appglobals.CUTOFF_UNIT)
        self.upper_cutoff_delegate = QSpinBoxItemDelegate(self, 0, 2000, appglobals.CUTOFF_UNIT)

        self.table.setItemDelegateForColumn(2, self.position_delegate)
        self.table.setItemDelegateForColumn(3, self.lower_cutoff_delegate)
        self.table.setItemDelegateForColumn(4, self.upper_cutoff_delegate)

        self.table.itemChanged.connect(self.save_filters)
    
    def add_filter_row(self):
        """Add row in table."""
        self.row_count = self.table.rowCount()
        self.table.insertRow(self.row_count)

    def remove_filter_row(self):
        """Remove selected rows from table."""
        for model_index in self.table.selectionModel().selection().indexes():
            index = QtCore.QPersistentModelIndex(model_index)
            self.table.removeRow(index.row())
        self.save_filters()
    
    def load_filters(self, filters: List[Dict[str, str]]):
        """Load contents of filters.json into table."""
        count = 0
        for f in filters:
            self.add_filter_row()

            self.table.setItem(count, 0, QtWidgets.QTableWidgetItem(f["Name"]))
            self.table.setItem(count, 1, QtWidgets.QTableWidgetItem(f["Brand"]))
            self.table.setItem(count, 2, QtWidgets.QTableWidgetItem(str(f["Wheel Position"])))
            self.table.setItem(count, 3, QtWidgets.QTableWidgetItem(str(f["Lower Cutoff"])))
            self.table.setItem(count, 4, QtWidgets.QTableWidgetItem(str(f["Upper Cutoff"])))

            count += 1
    
    def save_filters(self):
        """Save contents of table into filters.json."""
        if os.path.exists("filters.json"):
            os.remove("filters.json")
        filter_list = []
        for row in range(self.table.rowCount()):
            filter_dict = {}
            for col in range(self.table.columnCount()):
                header = str(self.table.horizontalHeaderItem(col).text())
                item = self.table.item(row, col)
                value = None

                # Save existing items with numeric strings as integers.
                if item is None:
                    pass
                elif col > 1 and item.text() not in ("", "None"):
                    value = int(item.text())
                elif isinstance(item.text(), str) and item.text() not in ("", "None"):
                    value = item.text()
                filter_dict.update({header: value})
            filter_list.append(filter_dict)
        with open("filters.json", "a") as f:
            json.dump(filter_list, f, indent=0)
        with open("filters.json", "r") as f:
            appglobals.filters = json.load(f)

        # Update filter model
        filter_names = []
        for f in appglobals.filters:
            filter_names.append(f["Name"])
        self.filter_list_model.setStringList(filter_names)

        self.filters_changed.emit()
