from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit
from PyQt5.QtCore import Qt, QRect, pyqtSignal 
from PyQt5.QtGui import QColor, QTextFormat, QPainter, QTextCursor
from view.cursor import Cursor
from mode.mode import Mode
from view.bar import LineNumberBar
from utils.utils import log, wlecome_text


class Editor(QPlainTextEdit):
    signal_update_status_bar = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mode = Mode()
        self.dispaly_welcome = False
        self.initUI()
        
        self.lineNumberBar = LineNumberBar(self)
        self.blockCountChanged.connect(self.updateLineNumberBarWidth)
        self.updateRequest.connect(self.updateLineNumberBar)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.welcome()

    def initUI(self):
        self.setStyleSheet("background-color: rgb(41, 44, 51);\
            color: rgb(171, 177, 189);")

    def welcome(self):
        self.setPlainText(wlecome_text)
        self.dispaly_welcome = True
        self.normal_mode()

    def set_mode(self, mode):
        self.mode.set_mode(mode)
        self.signal_update_status_bar.emit()

    def lineNumberBarWidth(self):
        digits = 1
        char_width = self.fontMetrics().width('9')
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = (char_width*8 if digits<=5 else char_width*(digits+3))
        return space

    def updateLineNumberBarWidth(self, _):
        self.setViewportMargins(self.lineNumberBarWidth(), 0, 0, 0)

    def updateLineNumberBar(self, rect, dy):
        if dy:
            self.lineNumberBar.scroll(0, dy)
        else:
            self.lineNumberBar.update(0, rect.y(), self.lineNumberBar.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberBarWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberBar.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberBarWidth(), cr.height()))

    def lineNumberBarPaintEvent(self, event):
        painter = QPainter(self.lineNumberBar)
        painter.fillRect(event.rect(), QColor(41, 44, 51))
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        char_width = self.fontMetrics().width('9')
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()

        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                if blockNumber == self.textCursor().blockNumber():
                    painter.setPen(QColor(172, 178, 190))
                else:
                    painter.setPen(QColor(75, 81, 97))
                painter.setFont(self.font())
                painter.drawText(0, top, self.lineNumberBar.width()-
                                 2*char_width, height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
    
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(45, 49, 59)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

            self.lineNumberBar.update()
        self.setExtraSelections(extraSelections)

    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.normal_mode()
        elif self.mode == 0:
            if event.key() == 73:
                if self.dispaly_welcome:
                    self.dispaly_welcome = False
                    self.setPlainText('')
                self.insert_mode()
            elif event.key() == 86:
                self.visual_mode()
            elif event.key() == 82:
                self.replace_mode()
            elif event.key() == 58:
                self.command_mode()
            elif event.key() == 72:
                self.textCursor().setPosition(self.textCursor().Left)
                log('Left')
            elif event.key() == 74:
                self.textCursor().setPosition(self.textCursor().Up)
                log('Up')
            elif event.key() == 75:
                self.textCursor().movePosition(self.textCursor().Down)
                log('Down')
            elif event.key() == 76:
                self.textCursor().movePosition(self.textCursor().Right)
                log('Right')
        elif self.mode == 1:
            if event.key() == Qt.Key_Tab:
                self.textCursor().insertText("    ")
                return
            super().keyPressEvent(event)

    def normal_mode(self):
        self.set_mode(0)
        self.setReadOnly(True)
        self.setTextInteractionFlags(self.textInteractionFlags() | Qt.TextSelectableByKeyboard)
    
    def insert_mode(self):
        self.set_mode(1)
        self.setReadOnly(False)

    def visual_mode(self):
        self.set_mode(2)
        self.setReadOnly(True)

    def replace_mode(self):
        self.set_mode(3)
        self.setReadOnly(False)

    def command_mode(self):
        self.set_mode(4)
        self.setReadOnly(True)
