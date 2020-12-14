from PySide6 import QtCore
from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyledItemDelegate, QDateTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox


class QDateTimeEditItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, time_spec=Qt.UTC):
        super().__init__(parent=parent)
        self.time_spec = time_spec
        self.format = "yyyy-MM-dd hh:mm"

    def createEditor(self, parent, option, index):
        editor = QDateTimeEdit(QtCore.QDate.currentDate().addDays(1), parent)
        editor.setDisplayFormat(self.format)
        editor.setTimeSpec(self.time_spec)
        return editor

    def setEditorData(self, editor, index):
        editor.setDateTime(QtCore.QDateTime.fromString(index.model().data(index, Qt.EditRole), self.format))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.dateTime().toString(self.format), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QComboBoxItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, items=()):
        super().__init__(parent=parent)
        self.items = items

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        if isinstance(self.items, QStringListModel):
            editor.setModel(self.items)
        else:
            editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        editor.setCurrentIndex(editor.findText(index.model().data(index, Qt.EditRole)))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QSpinBoxItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, minimum=0, maximum=99, suffix=""):
        super().__init__(parent=parent)
        self.min = minimum
        self.max = maximum
        self.suffix = suffix

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setMinimum(self.min)
        editor.setMaximum(self.max)
        editor.setSuffix(self.suffix)
        return editor

    def setEditorData(self, editor, index):
        data = index.model().data(index, Qt.EditRole)
        if data not in (None, "None"):
            editor.setValue(int(data))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def displayText(self, value, locale):
        if value != "None":
            return str(value) + self.suffix
        return ""
