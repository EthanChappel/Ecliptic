from PySide2 import QtCore
from PySide2.QtCore import Qt, QStringListModel
from PySide2.QtWidgets import QItemDelegate, QTimeEdit, QSpinBox, QComboBox


class QTimeEditItemDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def createEditor(self, parent, option, index):
        editor = QTimeEdit(parent)
        editor.setDisplayFormat("HH:mm:ss")
        return editor

    def setEditorData(self, editor, index):
        editor.setTime(QtCore.QTime.fromString(index.model().data(index, Qt.EditRole)))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.time().toString(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class QComboBoxItemDelegate(QItemDelegate):
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


class QSpinBoxItemDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        return editor

    def setEditorData(self, editor, index):
        editor.setValue(int(index.model().data(index, Qt.EditRole)))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.cleanText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
