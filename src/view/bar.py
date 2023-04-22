from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize

class LineNumberBar(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberBarWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberBarPaintEvent(event)
