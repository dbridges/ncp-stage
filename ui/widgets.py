from PyQt4 import QtGui, QtCore  # noqa


class MEANavigationWidget(QtGui.QWidget):
    """
    A widget which displays an MEA overview grid.
    """
    clicked = QtCore.pyqtSignal(object)

    mea_120_electrodes = ['f7', 'f8', 'f12', 'f11', 'f10', 'f9', 'e12', 'e11',
                          'e10', 'e9', 'd12', 'd11', 'd10', 'd9', 'c11', 'c10',
                          'b10', 'e8', 'c9', 'b9', 'a9', 'd8', 'c8', 'b8',
                          'a8', 'd7', 'c7', 'b7', 'a7', 'e7', 'f6', 'e6', 'a6',
                          'b6', 'c6', 'd6', 'a5', 'b5', 'c5', 'd5', 'a4', 'b4',
                          'c4', 'd4', 'b3', 'c3', 'c2', 'e5', 'd3', 'd2', 'd1',
                          'e4', 'e3', 'e2', 'e1', 'f4', 'f3', 'f2', 'f1', 'f5',
                          'g6', 'g5', 'g1', 'g2', 'g3', 'g4', 'h1', 'h2', 'h3',
                          'h4', 'j1', 'j2', 'j3', 'j4', 'k2', 'k3', 'l3', 'h5',
                          'k4', 'l4', 'm4', 'j5', 'k5', 'l5', 'm5', 'j6', 'k6',
                          'l6', 'm6', 'h6', 'g7', 'h7', 'm7', 'l7', 'k7', 'j7',
                          'm8', 'l8', 'k8', 'j8', 'm9', 'l9', 'k9', 'j9',
                          'l10', 'k10', 'k11', 'h8', 'j10', 'j11', 'j12', 'h9',
                          'h10', 'h11', 'h12', 'g8', 'g9', 'g10', 'g11', 'g12']

    def __init__(self, parent):
        super().__init__(parent)
        self.mea_120_columns = {'a':  0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
                                'f': 5, 'g': 6, 'h': 7, 'j': 8, 'k': 9,
                                'l': 10, 'm': 11}

    def paintEvent(self, event):
        d = min(self.width(), self.height())
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        font = p.font()
        font.setPixelSize(30)
        p.setFont(font)

        if self.width() > self.height():
            p.translate(self.width()/2 - 650*d/1300, 0)
        else:
            p.translate(0, self.height()/2 - 650*d/1300)
        p.scale(d/1300, d/1300)

        # Draw background
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(QtGui.QColor(167, 231, 255, 98))
        p.drawRoundedRect(0, 0, 1300, 1300, 65, 65)

        p.setBrush(QtGui.QColor(0, 98, 136))
        for tag in self.mea_120_electrodes:
            p.setPen(QtCore.Qt.NoPen)
            col = self.mea_120_columns[tag[0]]
            row = int(tag[1:]) - 1
            x = col*100 + 100
            y = row*100 + 100
            p.drawEllipse(QtCore.QPointF(x, y), 15, 15)
            p.setPen(QtGui.QColor(217, 38, 0))
            p.drawText(QtCore.QRectF(x-30, y-55, 60, 40),
                       QtCore.Qt.AlignCenter, tag.upper())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            w = self.width()
            h = self.height()
            spacing = min(w, h) / 13
            x = 5.5 - ((self.width() / 2 - event.x()) / spacing)
            y = 5.5 - ((self.height() / 2 - event.y()) / spacing)
            self.clicked.emit((x, y))
            event.accept()
