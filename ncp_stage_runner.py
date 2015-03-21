#!/usr/bin/env python3

import sys

from PyQt4 import QtCore, QtGui
from ncp_stage import MainWindow


if __name__ == '__main__':
    # See if com ports have been identified
    settings = QtCore.QSettings('UCSB', 'ncpstepper')
    settings.beginGroup('Stepper')
    x_motor_sn = settings.value('x_motor_sn', None)
    y_motor_sn = settings.value('y_motor_sn', None)
    if x_motor_sn is None:
        print('X motor identifier: ', end='')
        x_motor_sn = input()
        settings.setValue('x_motor_sn', x_motor_sn)
    if y_motor_sn is None:
        print('Y motor identifier: ', end='')
        y_motor_sn = input()
        settings.setValue('y_motor_sn', y_motor_sn)
    settings.endGroup()

    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(app)
    mainWindow.show()
    sys.exit(app.exec_())
