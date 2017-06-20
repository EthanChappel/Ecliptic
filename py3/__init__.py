#!/usr/bin/env python3
import sys
import traceback
from typing import Any
from PyQt5 import QtWidgets
from guistyle import switch_style

sys.dont_write_bytecode = True


def excepthook(exc_type: tuple, exc_val: Any, tracebackobj: traceback):
    messagebox = QtWidgets.QMessageBox()
    messagebox.setIcon(QtWidgets.QMessageBox.Critical)

    message = str("".join(traceback.format_tb(tracebackobj)))
    message_text = str(exc_type) + message + str(exc_val)
    print(message_text)
    messagebox.setWindowTitle("Solar System Sequencer - Exception")
    messagebox.setText("An exception occurred! Please copy the text in the details, then open a new issue at:")
    messagebox.setInformativeText("<a href='https://github.com/EthanChappel/Solar-System-Sequencer/issues'>"
                                  "https://github.com/EthanChappel/Solar-System-Sequencer/issues</a>")
    messagebox.setDetailedText(message_text)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    messagebox.exec_()

app = QtWidgets.QApplication(sys.argv)

switch_style(app, True)

sys.excepthook = excepthook
import mainwindow
widget = mainwindow.MainWindow()
widget.show()
app.setQuitOnLastWindowClosed(False)
sys.exit(app.exec_())
