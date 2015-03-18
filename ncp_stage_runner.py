#!/usr/bin/env python3

import sys
from PyQt4 import QtGui
from ncp_stage import MainWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow(app)
    mainWindow.show()
    sys.exit(app.exec_())
