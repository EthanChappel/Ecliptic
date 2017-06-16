from PyQt5 import QtGui


def switch_style(app, flag):
    """Set style of QApplication."""
    if flag:
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(85, 85, 85))
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(95, 95, 95))
        palette.setColor(QtGui.QPalette.Foreground, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Light, QtGui.QColor(110, 110, 110))
        palette.setColor(QtGui.QPalette.Dark, QtGui.QColor(75, 75, 75))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(255, 50, 50))
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(95, 95, 95))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(200, 80, 80))
        palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))

        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Button, QtGui.QColor(75, 75, 75))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(200, 200, 200))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(200, 200, 200))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, QtGui.QColor(80, 80, 80))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Foreground, QtGui.QColor(200, 200, 200))

        app.setStyleSheet("QDockWidget{"
                          "titlebar-normal-icon: url(:/icons/ic_open_in_new_white_48px.svg);"
                          "titlebar-close-icon: url(:/icons/ic_close_white_48px.svg);}")

        app.setPalette(palette)
        app.setStyle("Fusion")
    elif not flag:
        app.setStyle("WindowsVista")
