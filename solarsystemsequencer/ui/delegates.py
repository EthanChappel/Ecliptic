from PySide2 import QtCore
from PySide2.QtCore import Qt, QStringListModel
from PySide2.QtWidgets import QStyledItemDelegate, QDateEdit, QTimeEdit, QSpinBox, QComboBox


class QDateEditItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, time_spec=Qt.UTC):
        super().__init__(parent=parent)
        self.time_spec = time_spec
        self.format = "yyyy-MM-dd"

    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setDisplayFormat(self.format)
        editor.setTimeSpec(self.time_spec)
        editor.setCalendarPopup(True)
        return editor

    def setEditorData(self, editor, index):
        editor.setDate(QtCore.QDate.fromString(index.model().data(index, Qt.EditRole), self.format))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.date().toString(self.format), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QTimeEditItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, time_spec=Qt.UTC):
        super().__init__(parent=parent)
        self.time_spec = time_spec
        self.format = "HH:mm"

    def createEditor(self, parent, option, index):
        editor = QTimeEdit(parent)
        editor.setDisplayFormat(self.format)
        editor.setTimeSpec(self.time_spec)
        return editor

    def setEditorData(self, editor, index):
        editor.setTime(QtCore.QTime.fromString(index.model().data(index, Qt.EditRole)))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.time().toString(self.format), Qt.EditRole)

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
