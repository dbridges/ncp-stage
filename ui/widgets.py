from PyQt4 import QtGui, QtCore  # noqa


class MEANavigationWidget(QtGui.QWidget):
    """
    A widget which displays an MEA overview grid.
    """
    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, event):
        d = min(self.width(), self.height())
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.width() > self.height():
            p.translate(self.width()/2 - 650*d/1300, 0)
        else:
            p.translate(0, self.height()/2 - 650*d/1300)
        p.scale(d/1300, d/1300)

        for i in range(12):
            for j in range(12):
                p.drawEllipse(QtCore.QPointF(i*100 + 100, j*100 + 100), 15, 15)
