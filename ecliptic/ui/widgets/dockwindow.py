from PySide6 import QtCore, QtWidgets


class DockWindow(QtWidgets.QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.topLevelChanged.connect(self.set_flags)

    def set_flags(self):
        if self.isFloating():
            flags = QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint
            if QtWidgets.QDockWidget.DockWidgetClosable & self.features():
                flags = flags | QtCore.Qt.WindowCloseButtonHint
            self.setWindowFlags(flags)
            self.show()
