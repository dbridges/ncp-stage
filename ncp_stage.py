#!/usr/bin/env python3

from PyQt4 import QtGui, QtCore  # noqa
from ui.main_window import Ui_MainWindow

import stepper


# Try to load local port definitions
try:
    import stepper_ports
    x_motor_port = stepper_ports.x_motor_port
    y_motor_port = stepper_ports.y_motor_port
except ImportError:
    x_motor_port = None
    y_motor_port = None


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    Subclass of QMainWindow
    """
    def __init__(self, parent_app, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app = parent_app

        # UI initialization
        self.setupUi(self)
        self.load_settings()

        # Hardware initialization
        self.x_motor = stepper.ThorStepper(port='/dev/ttyUSB1')
        self.x_motor.event.connect(self.on_xMotor_event,
                                   QtCore.Qt.QueuedConnection)
        self.x_motor.start()
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.tick)
        self._timer.start(100)

    def tick(self):
        self.x_motor.update()

    def on_xMotor_event(self, event):
        event_type, data = event
        if event_type == 'pos':
            self.xPosSpinBox.setValue(data * 1000)

    def load_settings(self):
        # Load gui settings and restore window geometery
        settings = QtCore.QSettings('UCSB', 'ncpstepper')
        try:
            settings.beginGroup('MainWindow')
            self.restoreGeometry(settings.value('geometry'))
            settings.endGroup()
        except:
            pass

    def save_settings(self):
        settings = QtCore.QSettings('UCSB', 'ncpstepper')
        settings.beginGroup('MainWindow')
        settings.setValue('geometry', self.saveGeometry())
        settings.endGroup()

    def closeEvent(self, event):
        """
        Called when window is trying to be closed.  Call event.accept() to
        allow the window to be closed.
        """
        self.x_motor.stop()
        self.save_settings()
        event.accept()
