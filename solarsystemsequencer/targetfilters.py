import json
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import ui_targetfilters
import appglobals


class TargetFilters(QtWidgets.QDialog, ui_targetfilters.Ui_TargetFilters):
    def __init__(self, default=0):
        # TODO: Make dialog function!
        super(TargetFilters, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.size())

        self.filters_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.filters_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.targets_combobox.addItems(appglobals.targets_tuple)
        self.targets_combobox.setCurrentIndex(default)

        self.targets_combobox.currentIndexChanged.connect(self.load)

        self.load()

        self.exec_()

    def add_row(self):
        """Add row in filters_table."""
        row_count = self.filters_table.rowCount()
        self.filters_table.insertRow(row_count)

        # Create QComboBox for Use Column
        use_combobox = QtWidgets.QComboBox()
        use_combobox.addItems(("Yes", "No"))
        use_combobox.setCurrentIndex(0)

        # Create QSpinBox for Exposure Column
        exposure_spinbox = QtWidgets.QSpinBox()
        exposure_spinbox.setSuffix("ms")

        # Create QSpinBox for Gain Column
        gain_spinbox = QtWidgets.QSpinBox()
        gain_spinbox.setSuffix("e/adu")

        # Create QSpinBox for Integration Column
        integration_spinbox = QtWidgets.QSpinBox()
        integration_spinbox.setSuffix("s")

        use_combobox.currentIndexChanged.connect(lambda: self.save(self.targets_combobox.currentText()))
        exposure_spinbox.editingFinished.connect(lambda: self.save(self.targets_combobox.currentText()))
        gain_spinbox.editingFinished.connect(lambda: self.save(self.targets_combobox.currentText()))
        integration_spinbox.editingFinished.connect(lambda: self.save(self.targets_combobox.currentText()))

        # Add widgets to their cells
        self.filters_table.setCellWidget(row_count, 0, use_combobox)
        self.filters_table.setCellWidget(row_count, 1, exposure_spinbox)
        self.filters_table.setCellWidget(row_count, 2, gain_spinbox)
        self.filters_table.setCellWidget(row_count, 3, integration_spinbox)

    def load(self):
        self.filters_table.setRowCount(0)
        count = 0
        filters = []
        for f in appglobals.filters:
            self.add_row()

            self.filters_table.cellWidget(count, 0).blockSignals(True)
            self.filters_table.cellWidget(count, 1).blockSignals(True)
            self.filters_table.cellWidget(count, 2).blockSignals(True)
            self.filters_table.cellWidget(count, 3).blockSignals(True)
            try:
                use = appglobals.presets[self.targets_combobox.currentText()][f["Name"]]["Use"]
                use = self.filters_table.cellWidget(count, 0).findText(use, QtCore.Qt.MatchFixedString)
                exposure = int(appglobals.presets[self.targets_combobox.currentText()][f["Name"]]["Exposure"])
                gain = int(appglobals.presets[self.targets_combobox.currentText()][f["Name"]]["Gain"])
                integration = int(appglobals.presets[self.targets_combobox.currentText()][f["Name"]]["Integration"])

                self.filters_table.cellWidget(count, 0).setCurrentIndex(use)
                self.filters_table.cellWidget(count, 1).setValue(exposure)
                self.filters_table.cellWidget(count, 2).setValue(gain)
                self.filters_table.cellWidget(count, 3).setValue(integration)
            except KeyError:
                pass

            self.filters_table.cellWidget(count, 0).blockSignals(False)
            self.filters_table.cellWidget(count, 1).blockSignals(False)
            self.filters_table.cellWidget(count, 2).blockSignals(False)
            self.filters_table.cellWidget(count, 3).blockSignals(False)

            filters.append(f.get("Name"))

            count += 1
        self.filters_table.setVerticalHeaderLabels(filters)

    def save(self, target):
        filters = {}
        for r in range(self.filters_table.rowCount()):
            settings = {}
            row = str(self.filters_table.verticalHeaderItem(r).text())
            for c in range(self.filters_table.columnCount()):
                header = str(self.filters_table.horizontalHeaderItem(c).text())
                try:
                    value = str(self.filters_table.cellWidget(r, c).cleanText())
                except AttributeError:
                    value = str(self.filters_table.cellWidget(r, c).currentText())
                settings[header] = value
            filters[row] = settings
            appglobals.presets[target] = filters
        with open("presets.json", "w") as f:
            json.dump(appglobals.presets, f, indent=2)
