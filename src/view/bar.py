'''
All kinds of bars in the main window.
'''

from PyQt5.QtWidgets import QWidget, QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class LineNumberBar(QWidget):
    '''
    Line number bar class
    '''

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        '''
        Return line number bar width
        '''
        return QSize(self.editor.lineNumberBarWidth(), 0)

    def paintEvent(self, event):
        '''
        Paint line number bar
        '''
        self.editor.lineNumberBarPaintEvent(event)


class ToolBar(QToolBar):
    '''
    Tool bar class
    '''

    def __init__(self, wd, parent=None):
        '''
        Icon, status tip and trigger of each button
        '''
        super().__init__(parent)
        self.wd = wd
        self.setIconSize(QSize(16, 16))

        # file
        button_new = QAction(QIcon("./assets/icon/new"), "New File", self)
        button_new.setStatusTip("New File")
        button_new.triggered.connect(wd.editor.keyPressEvent)
        self.addAction(button_new)

        button_open_file = QAction(
            QIcon("./assets/icon/open_file"), "Open File", self)
        button_open_file.setStatusTip("Open File")
        button_open_file.triggered.connect(wd.open_file)
        self.addAction(button_open_file)

        button_open_folder = QAction(
            QIcon("./assets/icon/open_folder"), "Open Folder", self)
        button_open_folder.setStatusTip("Open Folder")
        button_open_folder.triggered.connect(wd.open_folder)
        self.addAction(button_open_folder)

        button_save = QAction(QIcon("./assets/icon/save"), "Save File", self)
        button_save.setStatusTip(f"Save File")
        button_save.triggered.connect(wd.save_file)
        self.addAction(button_save)

        button_save_as = QAction(
            QIcon("./assets/icon/save_as"), "Save File As", self)
        button_save_as.setStatusTip("Save File As")
        button_save_as.triggered.connect(wd.save_as)
        self.addAction(button_save_as)

        button_close_file = QAction(
            QIcon("./assets/icon/close_file"), "Close File", self)
        button_close_file.setStatusTip("Close File")
        button_close_file.triggered.connect(wd.close_file)
        self.addAction(button_close_file)

        button_close_folder = QAction(
            QIcon("./assets/icon/close_folder"), "Close Folder", self)
        button_close_folder.setStatusTip("Close Folder")
        button_close_folder.triggered.connect(wd.close_folder)
        self.addAction(button_close_folder)

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

        button_replace = QAction(
            QIcon("./assets/icon/replace"), "Replace", self)
        button_replace.setStatusTip("Replace")
        button_replace.triggered.connect(wd.rpl)

        button_replace_all = QAction(
            QIcon("./assets/icon/replace_all"), "Replace All", self)
        button_replace_all.setStatusTip("Replace All")
        button_replace_all.triggered.connect(wd.rpl_all)

        self.addAction(button_find)
        self.addWidget(wd.find_bar)
        self.addAction(button_before)
        self.addAction(button_next)
        self.addWidget(wd.replace_bar)
        # self.addAction(button_replace)
        self.addAction(button_replace_all)
        self.addWidget(wd.jump_bar)

        # miscellaneous
        self.addSeparator()

        button_terminal = QAction(
            QIcon("./assets/icon/terminal"), "Terminal", self)
        button_terminal.setStatusTip("Open Terminal")
        button_terminal.triggered.connect(wd.toggle_terminal)
        self.addAction(button_terminal)

        button_info = QAction(QIcon("./assets/icon/info"), "Info", self)
        button_info .setStatusTip("Info")
        button_info.triggered.connect(wd.show_info)
        self.addAction(button_info)
