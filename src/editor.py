from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QTextCursor
from PyQt5.QtWidgets import QTextEdit

class Editor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

