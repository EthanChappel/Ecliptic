from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyledItemDelegate, QSizePolicy, QFrame, QPushButton, QLineEdit, QHBoxLayout
import res_rc


class QWindowEditorDelegate(QStyledItemDelegate):
    def __init__(self, window, parent=None):
        super().__init__(parent=parent)

        self.window = window

    def createEditor(self, parent, option, index):
        editor = QFrame(parent)
        layout = QHBoxLayout(editor)
        text = QLineEdit(parent=editor)
        button = QPushButton(QIcon(":/icons/edit-white-48dp.svg"), "", parent=editor)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        editor.setLayout(layout)

        text.setFrame(False)
        text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        layout.addWidget(text)
        layout.addWidget(button)

        button.clicked.connect(self.edit_dialog)
        
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
    
    def edit_dialog(self):
        dialog = self.window()
        dialog.exec_()