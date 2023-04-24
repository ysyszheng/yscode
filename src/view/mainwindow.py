import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from view.editor import Editor
from view.bar import ToolBar
from utils.utils import log
from syntax.py import Highlighter as PythonHighlighter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = Editor()
        self.hightlighter = PythonHighlighter(self.editor.document())
        self.path = None
        self.initUI()
        self.update_title()
        self.update_status_bar()

        self.editor.cursorPositionChanged.connect(self.update_status_bar)

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('./assets/icons/logo.png'))
        self.setCentralWidget(self.editor)
        self.statusBar().setStyleSheet("background-color: rgb(31, 34, 39);\
                                       color: rgb(143, 149, 162);")

        self.set_font()
        self.set_menu()

        toolbar = ToolBar(self)
        self.addToolBar(toolbar)

    def set_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        edit_menu = menu.addMenu("Edit")
        view_menu = menu.addMenu("View")
        window_menu = menu.addMenu("Window")
        help_menu = menu.addMenu("Help")

        # File Menu
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(save_as_action)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(quit_action)

        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        save_as_action.triggered.connect(self.save_as)
        quit_action.triggered.connect(self.quit_app)

        # Edit Menu
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)

        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)

        cut_action.triggered.connect(self.editor.cut)
        copy_action.triggered.connect(self.editor.copy)
        paste_action.triggered.connect(self.editor.paste)
        undo_action.triggered.connect(self.editor.undo)
        redo_action.triggered.connect(self.editor.redo)

        # View Menu
        toggle_statusbar_action = QAction("Toggle Statusbar", self)
        toggle_statusbar_action.setShortcut("Ctrl+Shift+T")
        view_menu.addAction(toggle_statusbar_action)

        toggle_sidebar_action = QAction("Toggle Sidebar", self)
        toggle_sidebar_action.setShortcut("Ctrl+Alt+T")
        view_menu.addAction(toggle_sidebar_action)

        # Window Menu
        minimize_action = QAction("Minimize", self)
        minimize_action.setShortcut("Ctrl+M")
        window_menu.addAction(minimize_action)

        maximize_action = QAction("Maximize", self)
        maximize_action.setShortcut("Ctrl+Shift+M")
        window_menu.addAction(maximize_action)

        # Help Menu
        about_action = QAction("About", self)
        about_action.setShortcut("Ctrl+I")
        help_menu.addAction(about_action)

    def set_font(self):
        font = QFont("Monaco", 14)
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.editor.setFont(font)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if file_path:
            with open(file_path, 'r') as file:
                self.editor.setPlainText(file.read())
            self.path = file_path
            self.update_title()
        if self.editor.dispaly_welcome:    
            self.editor.dispaly_welcome = False
            self.editor.setReadOnly(False)

    def save_file(self):
        if self.path is None:
            self.save_as()
        else:
            with open(self.path, 'w') as file:
                file.write(self.editor.toPlainText())

    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.editor.toPlainText())
            self.path = file_path
            self.update_title()

    def close_file(self):
        self.path = None
        self.editor.setPlainText("")
        self.update_title()

    def quit_app(self):
        if self.editor.document().isModified():
            reply = QMessageBox.question(self, "Save?", "Do you want to save before quitting?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
                self.close()
            elif reply == QMessageBox.No:
                self.close()
        else:
            self.close()

    def update_title(self):
        self.setWindowTitle(
            "%s - YSCODE" % (os.path.basename(self.path) if self.path else "Untitled"))

    def update_status_bar(self):
        self.statusBar().showMessage("Ln %d, Col %d" % (self.editor.textCursor(
        ).blockNumber() + 1, self.editor.textCursor().columnNumber()))

    def show_info(self):
        QMessageBox.information(
            self, "About YSCODE", "YSCODE is a simple text editor.<br>Developed by Yusen Zheng.")

