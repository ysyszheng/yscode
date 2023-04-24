from PyQt5.QtWidgets import QWidget, QToolBar, QAction
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize

class LineNumberBar(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberBarWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberBarPaintEvent(event)

class ToolBar(QToolBar):
    def __init__(self, wd, parent=None):
        super().__init__(parent)
        self.wd = wd
        self.setIconSize(QSize(16, 16))
        
        # file
        button_new = QAction(QIcon("./assets/icon/new"), "New File", self)
        button_new.setStatusTip("New File")
        button_new.triggered.connect(wd.editor.keyPressEvent)
        self.addAction(button_new)

        button_open = QAction(QIcon("./assets/icon/open"), "Open File", self)
        button_open.setStatusTip("Open File")
        button_open.triggered.connect(wd.open_file)
        self.addAction(button_open)

        button_save = QAction(QIcon("./assets/icon/save"), "Save File", self)
        button_save.setStatusTip(f"Save File")
        button_save.triggered.connect(wd.save_file)
        self.addAction(button_save)

        button_save_as = QAction(QIcon("./assets/icon/save_as"), "Save File As", self)
        button_save_as.setStatusTip("Save File As")
        button_save_as.triggered.connect(wd.save_as)
        self.addAction(button_save_as)

        button_close = QAction(QIcon("./assets/icon/close"), "Close File", self)
        button_close.setStatusTip("Close File")
        button_close.triggered.connect(wd.close_file)
        self.addAction(button_close)

        self.addSeparator()

        # edit
        button_cut = QAction(QIcon("./assets/icon/cut"), "Cut", self)
        button_cut.setStatusTip("Cut")
        button_cut.triggered.connect(wd.editor.cut)
        self.addAction(button_cut)

        button_copy = QAction(QIcon("./assets/icon/copy"), "Copy", self)
        button_copy.setStatusTip("Copy")
        button_copy.triggered.connect(wd.editor.copy)
        self.addAction(button_copy)

        button_paste = QAction(QIcon("./assets/icon/paste"), "Paste", self)
        button_paste.setStatusTip("Paste")
        button_paste.triggered.connect(wd.editor.paste)
        self.addAction(button_paste)

        button_undo = QAction(QIcon("./assets/icon/undo"), "Undo", self)
        button_undo.setStatusTip("Undo")
        button_undo.triggered.connect(wd.editor.undo)
        self.addAction(button_undo)

        button_redo = QAction(QIcon("./assets/icon/redo"), "Redo", self)
        button_redo.setStatusTip("Redo")
        button_redo.triggered.connect(wd.editor.redo)
        self.addAction(button_redo)

        self.addSeparator()

        # find and replace
        button_find = QAction(QIcon("./assets/icon/find"), "Find", self)
        button_find.setStatusTip("Find")
        button_find.setEnabled(False)

        button_before = QAction(QIcon("./assets/icon/before"), "Before", self)
        button_before.setStatusTip("Find Before")
        button_before.triggered.connect(wd.fnd_before)

        button_next = QAction(QIcon("./assets/icon/next"), "Next", self)
        button_next.setStatusTip("Find Next")
        button_next.triggered.connect(wd.fnd_next)

        button_replace = QAction(QIcon("./assets/icon/replace"),"Replace", self)
        button_replace.setStatusTip("Replace")
        button_replace.triggered.connect(wd.rpl)

        button_replace_all = QAction(QIcon("./assets/icon/replace_all"), "Replace All", self)
        button_replace_all.setStatusTip("Replace All")
        button_replace_all.triggered.connect(wd.rpl_all)

        self.addAction(button_find)
        self.addWidget(wd.find_bar)
        self.addAction(button_before)
        self.addAction(button_next)
        self.addWidget(wd.replace_bar)
        self.addAction(button_replace)
        self.addAction(button_replace_all)

        # miscellaneous
        self.addSeparator()

        button_info = QAction(QIcon("./assets/icon/info"), "Info", self)
        button_info .setStatusTip("Info")
        button_info.triggered.connect(wd.show_info)
        self.addAction(button_info)
