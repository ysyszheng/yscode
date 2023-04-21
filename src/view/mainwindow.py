import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction
from PyQt5.QtGui import QIcon, QTextCursor, QFont

from editor import CustomTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Untitled - MEOW Editor")
        self.setGeometry(300, 300, 800, 600)
        # self.setWindowIcon(QIcon('icon.png'))

        self.text_edit = CustomTextEdit()
        self.setCentralWidget(self.text_edit)

        self.statusBar()

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

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(quit_action)

        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        quit_action.triggered.connect(self.quit_app)

        # Edit Menu
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)

        # View Menu
        toggle_toolbar_action = QAction("Toggle Toolbar", self)
        toggle_toolbar_action.setShortcut("Ctrl+T")
        view_menu.addAction(toggle_toolbar_action)

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
        font = QFont("Courier New")
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.editor.setFont(font)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if file_path:
            with open(file_path, 'r') as file:
                self.text_edit.setText(file.read())

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def quit_app(self):
        pass
    