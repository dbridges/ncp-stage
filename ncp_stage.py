#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore  # noqa
from ui.main_window import Ui_MainWindow


# Try to load local port definitions
try:
    import ncp_ports
    controller_port = ncp_ports.controller_port
except ImportError:
    controller_port = None


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Subclass of QMainWindow
    """
    def __init__(self, parent_app, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = parent_app

        # UI initialization
        self.setupUi(self)

        # Hardware initialization

    def closeEvent(self, event):
        """
        Called when window is trying to be closed.  Call event.accept() to
        allow the window to be closed.
        """
        event.accept()
