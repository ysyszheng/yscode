from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QColor, QTextFormat, QPainter, QTextBlockFormat
from view.bar import LineNumberBar
from utils.utils import log, welcome_text


class Editor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.display_welcome = False
        self.path = None
        self.blockFormat = QTextBlockFormat()
        self.initUI()
        
        self.lineNumberBar = LineNumberBar(self)
        self.blockCountChanged.connect(self.updateLineNumberBarWidth)
        self.updateRequest.connect(self.updateLineNumberBar)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.welcome()

    def initUI(self):
        self.setStyleSheet("background-color: rgb(41, 44, 51);\
            color: rgb(171, 177, 189);")
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

    def welcome(self):
        self.setPlainText(welcome_text)
        self.display_welcome = True
        self.setReadOnly(True)

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
                painter.drawText(0, float(top), float(self.lineNumberBar.width()-
                                 2*char_width), float(height), Qt.AlignRight, number)

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

    def indent(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.insertText("    ")
        cursor.endEditBlock()

    def keyPressEvent(self, event):
        if self.display_welcome:
            self.setPlainText("")
            self.display_welcome = False
            self.setReadOnly(False)
            return
        if event.key() == Qt.Key_Tab:
            self.textCursor().insertText("    ")
            return
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.textCursor()
            block = cursor.block()
            previous_text = block.text()
            index = 0
            while index < len(previous_text) and previous_text[index] == " ":
                index += 1
            previous_indent = previous_text[:index]
            self.blockFormat = QTextBlockFormat()
            self.blockFormat.setIndent(index / 4)
            cursor.insertBlock(self.blockFormat)
            cursor.insertText(previous_indent)
        else:
            super().keyPressEvent(event)
