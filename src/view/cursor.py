from PyQt5 import QtCore, QtGui

class BlinkBoxCursor(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BlinkBoxCursor, self).__init__(parent)
        self.setFixedSize(QtGui.QFontMetrics(QtGui.QFont()).size(QtCore.Qt.TextSingleLine, ' '))
        self.is_visible = True
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.toggle_visibility)
        self.timer.start(500)

    def paintEvent(self, event):
        if self.is_visible:
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        self.update()