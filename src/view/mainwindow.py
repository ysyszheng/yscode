import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from view.editor import Editor
from mode.mode import Mode
from utils.utils import log

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = Editor()
        self.mode = self.editor.mode # copy mode from editor
        self.path = None
        self.initUI()

        self.editor.signal_update_status_bar.connect(self.update_status_bar)

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('./assets/icons/logo.png'))

        self.set_font()
        self.set_menu()

        self.setCentralWidget(self.editor)
        self.update_title()

        self.statusBar().setStyleSheet("background-color: rgb(31, 34, 39);\
                                       color: rgb(143, 149, 162);")
        self.update_status_bar()

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
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)

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

    def quit_app(self):
        if self.editor.document().isModified():
            reply = QMessageBox.question(self, "Save?", "Do you want to save before quitting?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
                self.close()
            elif reply == QMessageBox.No:
                self.close()
        else:
            self.close()

    def update_title(self):
        self.setWindowTitle("%s - YSCODE" % (os.path.basename(self.path) if self.path else "Untitled"))

    def update_status_bar(self):
        if self.mode != 4: # if not in command mode
            self.statusBar().showMessage(f"-- {self.mode.get_mode_name()} --")
        else:
            self.statusBar().showMessage(f":")
        log(self.mode.get_mode_name())
