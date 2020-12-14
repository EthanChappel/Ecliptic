from PySide2 import QtCore
from PySide2.QtCore import Qt, QStringListModel
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QStyledItemDelegate, QSizePolicy, QFrame, \
    QPushButton, QDateTimeEdit, QLineEdit, QSpinBox, QComboBox, QHBoxLayout
import res_rc


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


class QScheduleParameterEditorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def createEditor(self, parent, option, index):
        editor = QFrame(parent)
        layout = QHBoxLayout(editor)
        text = QLineEdit(parent=editor)
        button = QPushButton(QIcon(":/icons/edit-white-48dp.svg"), "", parent=editor)

        layout.setMargin(0)
        layout.setSpacing(0)
        editor.setLayout(layout)

        text.setFrame(False)
        text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        layout.addWidget(text)
        layout.addWidget(button)
        
        return editor

    def setEditorData(self, editor, index):
        data = index.model().data(index, Qt.EditRole)
        if data not in (None, "None"):
            text = editor.findChildren(QLineEdit)[0]
            text.setText(data)

    def setModelData(self, editor, model, index):
        text = editor.findChildren(QLineEdit)[0]
        model.setData(index, text.text(), Qt.EditRole)
    
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
    
    def displayText(self, value, locale):
        if value == "None":
            return ""
        return value
