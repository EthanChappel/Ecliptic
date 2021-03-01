from PySide6 import QtCore, QtWidgets
from .uic.filter_settings import Ui_FilterSettingsFrame
from ..delegates.widgets import *
import appglobals


class FilterSettingsFrame(QtWidgets.QFrame, Ui_FilterSettingsFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.filter_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Create Delegates for columns in filters table.
        self.filter_delegate = QComboBoxItemDelegate(self, [f['Name'] for f in appglobals.filters])
        self.exposure_delegate = QDoubleSpinBoxItemDelegate(self)
        self.gain_delegate = QSpinBoxItemDelegate(self)
        self.bin_delegate = QComboBoxItemDelegate(self)
        self.limit_delegate = QSpinBoxItemDelegate(self)
        self.format_delegate = QComboBoxItemDelegate(self)

        # Set item delegates for columns in filters table.
        self.filter_table.setItemDelegateForColumn(0, self.filter_delegate)
        self.filter_table.setItemDelegateForColumn(1, self.exposure_delegate)
        self.filter_table.setItemDelegateForColumn(2, self.gain_delegate)
        self.filter_table.setItemDelegateForColumn(3, self.bin_delegate)
        self.filter_table.setItemDelegateForColumn(4, self.limit_delegate)
        self.filter_table.setItemDelegateForColumn(5, self.format_delegate)
    
    def add_filter_row(self):
        """Add row in filter_table."""
        self.row_count = self.filter_table.rowCount()
        self.filter_table.insertRow(self.row_count)

    def remove_filter_row(self):
        """Remove selected rows from filter_table."""
        for model_index in self.filter_table.selectionModel().selection().indexes():
            index = QtCore.QPersistentModelIndex(model_index)
            self.filter_table.removeRow(index.row())