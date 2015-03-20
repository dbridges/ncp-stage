from PyQt4 import QtGui, QtCore  # noqa

class MEANavigationWidget(QtGui.QWidget):
    """
    A widget which displays an MEA overview grid.
    """
    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, event):
        d = self.width()
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        transform = QtGui.QTransform()
        transform.scale(d/1300, d/1300)
        p.setTransform(transform)

        for i in range(12):
            for j in range(12):
                p.drawEllipse(QtCore.QPointF(i*100 + 100, j*100 + 100), 15, 15)

    def heightForWidth(self, w):
        return w
