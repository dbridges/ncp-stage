#!/usr/bin/env python3

import sys

from PyQt4 import QtGui, QtCore  # noqa
from ui.main_window import Ui_MainWindow

import stepper


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
        try:
            self.stage = stepper.XYStage(self)
            self.stage.velocity = self.jogSpeedSlider.value() / 10
        except IOError as e:
            message = QtGui.QMessageBox(self)
            message.setWindowTitle('Connection Error')
            message.setText(str(e))
            message.exec_()
            sys.exit()

        # Application initializations
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.tick)
        self._timer.start(150)

    def tick(self):
        self.stage.update()

    def on_xPos_changed(self, val):
        self.xPosSpinBox.setValue(val * 1000)

    def on_yPos_changed(self, val):
        self.yPosSpinBox.setValue(val * 1000)

    @QtCore.pyqtSlot()
    def on_zeroButton_pressed(self):
        self.stage.zero()

    @QtCore.pyqtSlot()
    def on_jogLeftButton_pressed(self):
        self.stage.start_move('x', 'forward')

    @QtCore.pyqtSlot()
    def on_jogLeftButton_released(self):
        self.stage.stop_move('x')

    @QtCore.pyqtSlot()
    def on_jogRightButton_pressed(self):
        self.stage.start_move('x', 'backward')

    @QtCore.pyqtSlot()
    def on_jogRightButton_released(self):
        self.stage.stop_move('x')

    @QtCore.pyqtSlot()
    def on_jogDownButton_pressed(self):
        self.stage.start_move('y', 'backward')

    @QtCore.pyqtSlot()
    def on_jogDownButton_released(self):
        self.stage.stop_move('y')

    @QtCore.pyqtSlot()
    def on_jogUpButton_pressed(self):
        self.stage.start_move('y', 'forward')

    @QtCore.pyqtSlot()
    def on_jogUpButton_released(self):
        self.stage.stop_move('y')

    @QtCore.pyqtSlot(int)
    def on_jogSpeedSlider_sliderMoved(self, val):
        self.stage.velocity = val / 10

    @QtCore.pyqtSlot()
    def on_homeButton_clicked(self):
        self.stage.home(center=True)

    @QtCore.pyqtSlot(object)
    def on_meaNavigationWidget_clicked(self, coord):
        # When stage is zeroed, should be centered on A4
        self.stage.x = -coord[0] / 1000
        self.stage.y = -(coord[1] - 300) / 1000

    @QtCore.pyqtSlot()
    def on_retractYButton_clicked(self):
        self.stage.retract_y()

    @QtCore.pyqtSlot()
    def on_returnYButton_clicked(self):
        self.stage.return_y()

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
        self.stage.stop()
        self.save_settings()
        event.accept()
