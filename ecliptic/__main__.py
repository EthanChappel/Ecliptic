#!/usr/bin/env python3
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import mainwindow

sys.dont_write_bytecode = True

app = QtWidgets.QApplication(sys.argv)

palette = QtGui.QPalette()
palette.setColor(QtGui.QPalette.Window, QtGui.QColor(50, 50, 50))
palette.setColor(QtGui.QPalette.Button, QtGui.QColor(60, 60, 60))
palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
palette.setColor(QtGui.QPalette.Light, QtGui.QColor(80, 80, 80))
palette.setColor(QtGui.QPalette.Dark, QtGui.QColor(50, 50, 50))
palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
palette.setColor(QtGui.QPalette.Link, QtGui.QColor(50, 50, 255))
palette.setColor(QtGui.QPalette.Base, QtGui.QColor(55, 55, 55))
palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(60, 140, 200))
palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))

palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QColor(40, 40, 40))
palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(200, 200, 200))
palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(200, 200, 200))
palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(80, 80, 80))
palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(200, 200, 200))

app.setStyleSheet("""
    QDockWidget {
       titlebar-normal-icon: url(:/icons/ic_open_in_new_white_48px.svg);
       titlebar-close-icon: url(:/icons/ic_close_white_48px.svg);
    }
""")
app.setPalette(palette)
app.setStyle("Fusion")

widget = mainwindow.MainWindow()
widget.show()
sys.exit(app.exec_())
