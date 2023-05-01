'''
Main Window
'''

import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QMessageBox, QLineEdit, QFileSystemModel, QTreeView, QSplitter, QMenu, QInputDialog
from PyQt5.QtGui import QFont, QIcon, QTextDocument, QTextCursor
from PyQt5.QtCore import Qt, QFileInfo, QDir
import shutil
from view.editor import Editor
from view.bar import ToolBar
from view.terminal import Terminal
from utils.utils import log
from syntax.py import Highlighter as PythonHighlighter


class MainWindow(QMainWindow):
    '''
    Main Window Class
    '''

    def __init__(self):
        super().__init__()
        self.splitter = QSplitter()
        self.editor = Editor()
        self.terminal = Terminal()
        self.hightlighter = PythonHighlighter(self.editor.document())
        self.dir = None
        self.find_bar = QLineEdit(self)
        self.replace_bar = QLineEdit(self)
        self.jump_bar = QLineEdit(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree = QTreeView()
        self.fnd = False

        self.initUI()
        self.update_title()
        self.update_status_bar()

        self.editor.cursorPositionChanged.connect(self.update_status_bar)
        self.editor.cursorPositionChanged.connect(self.reset_fnd)
        self.find_bar.returnPressed.connect(self.fnd_next)
        self.jump_bar.returnPressed.connect(self.jump)
        self.replace_bar.returnPressed.connect(self.rpl)
        self.tree.doubleClicked.connect(self.open_file_from_tree)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_tree_menu)

    def initUI(self):
        '''
        Initialize UI
        '''
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('./assets/icons/logo.png'))

        self.setCentralWidget(self.splitter)
        self.splitter.setStyleSheet("background-color: rgb(63, 68, 81);")

        self.statusBar().setStyleSheet("background-color: rgb(31, 34, 39);\
                                       color: rgb(143, 149, 162);")
        self.set_font()
        self.set_menu()
        toolbar = ToolBar(self)
        self.addToolBar(toolbar)
        self.find_bar.setPlaceholderText("Enter to find")
        self.replace_bar.setPlaceholderText("Enter to replace")
        self.jump_bar.setPlaceholderText("Enter line number")
        self.find_bar.setFixedWidth(150)
        self.replace_bar.setFixedWidth(150)
        self.jump_bar.setFixedWidth(150)

        self.tree.setModel(self.model)
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setStyleSheet("background-color: rgb(34, 37, 42);\
            color: rgb(154, 159, 170);\
            QTreeView::branch:selected {background-color: rgb(255, 0, 0);}")
        self.tree.setHeaderHidden(True)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        splitter1 = QSplitter()
        splitter1.addWidget(self.tree)
        splitter2 = QSplitter()
        splitter2.addWidget(self.editor)
        splitter2.addWidget(self.terminal)
        splitter2.setOrientation(Qt.Vertical)
        splitter2.setSizes([int(self.height() * (2/3)),
                           self.height() - int(self.height() * (2/3))])

        self.splitter.addWidget(splitter1)
        self.splitter.addWidget(splitter2)
        self.splitter.setSizes(
            [int(self.width() * 0.2), self.width() - int(self.width() * 0.2)])
        self.tree.hide()
        self.terminal.hide()

    def set_menu(self):
        '''
        Set Menu
        '''
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        edit_menu = menu.addMenu("Edit")
        view_menu = menu.addMenu("View")
        window_menu = menu.addMenu("Window")
        help_menu = menu.addMenu("Help")

        # File Menu
        open_file_action = QAction("Open File", self)
        open_file_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_file_action)

        open_folder_action = QAction("Open Folder", self)
        open_folder_action.setShortcut("Ctrl+Shift+O")
        file_menu.addAction(open_folder_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        file_menu.addAction(save_as_action)

        close_action = QAction("Close", self)
        close_action.setShortcut("Ctrl+W")
        file_menu.addAction(close_action)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(quit_action)

        open_file_action.triggered.connect(self.open_file)
        open_folder_action.triggered.connect(self.open_folder)
        save_action.triggered.connect(self.save_file)
        save_as_action.triggered.connect(self.save_as)
        close_action.triggered.connect(self.close_file)
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
        toggle_sidebar_action = QAction("Toggle Sidebar", self)
        toggle_sidebar_action.setShortcut("Ctrl+B")
        view_menu.addAction(toggle_sidebar_action)
        toggle_sidebar_action.triggered.connect(self.toggle_sidebar)

        toggle_terminal_action = QAction("Toggle Terminal", self)
        toggle_terminal_action.setShortcut("Ctrl+T")
        view_menu.addAction(toggle_terminal_action)
        toggle_terminal_action.triggered.connect(self.toggle_terminal)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        view_menu.addAction(zoom_in_action)
        zoom_in_action.triggered.connect(self.editor.zoomIn)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        view_menu.addAction(zoom_out_action)
        zoom_out_action.triggered.connect(self.editor.zoomOut)

        # Window Menu
        minimize_action = QAction("Minimize", self)
        minimize_action.setShortcut("Ctrl+M")
        window_menu.addAction(minimize_action)
        minimize_action.triggered.connect(self.showMinimized)

        maximize_action = QAction("Maximize", self)
        maximize_action.setShortcut("Ctrl+Shift+M")
        window_menu.addAction(maximize_action)
        maximize_action.triggered.connect(self.showMaximized)

        # Help Menu
        about_action = QAction("About", self)
        about_action.setShortcut("Ctrl+I")
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_info)

    def set_font(self):
        '''
        Set Font
        '''
        font = QFont("Consolas", 14)
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.editor.setFont(font)

    def open_file(self):
        '''
        Open File
        '''
        if self.editor.document().isModified():
            reply = QMessageBox.question(self, "Save?", "Do you want to save before closing?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
                self.open_file_helper()
            elif reply == QMessageBox.No:
                self.open_file_helper()
        else:
            self.open_file_helper()

    def open_folder(self):
        '''
        Open Folder
        '''
        dir_path = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if dir_path:
            self.model.setRootPath(dir_path)
            self.tree.setRootIndex(self.model.index(dir_path))
            self.tree.sortByColumn(0, Qt.AscendingOrder)
            self.dir = dir_path
            self.update_title()
            self.tree.show()
            self.terminal.current_directory = dir_path
        if self.editor.display_welcome:
            self.editor.display_welcome = False
            self.editor.setReadOnly(False)

    def open_file_from_tree(self, index):
        '''
        Open File From File Tree
        '''
        file_path = self.model.filePath(index)
        if QFileInfo(file_path).isDir():
            return
        try:
            self.close_file()
            with open(file_path, 'r') as file:
                self.editor.setPlainText(file.read())
            self.editor.path = file_path
            self.update_title()
        except UnicodeDecodeError:
            QMessageBox.warning(
                self, "Warning", "Cannot open non-UTF-8 text files")

    def save_file(self):
        '''
        Save File
        '''
        if self.editor.path is None:
            self.save_as()
        else:
            with open(self.editor.path, 'w') as file:
                file.write(self.editor.toPlainText())

    def save_as(self):
        '''
        Save As
        '''
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.editor.toPlainText())
            self.editor.path = file_path
            self.update_title()

    def close_file(self):
        '''
        Close File
        '''
        if self.editor.document().isModified():
            reply = QMessageBox.question(self, "Save?", "Do you want to save before closing?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_file()
                self.close_file_helper()
            elif reply == QMessageBox.No:
                self.close_file_helper()
        else:
            self.close_file_helper()

    def close_file_helper(self):
        '''
        Remove File Path, Clear Editor, and Update Title
        '''
        self.editor.path = None
        self.editor.setPlainText("")
        self.update_title()

    def close_folder(self):
        '''
        Close Folder
        '''
        self.dir = None
        self.editor.path = None
        self.editor.setPlainText("")
        self.tree.hide()
        self.update_title()

    def quit_app(self):
        '''
        Quit Application
        '''
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
        '''
        Update Title
        '''
        self.setWindowTitle(
            "%s - %s" % (os.path.basename(self.editor.path) if self.editor.path else "Untitled",
                         os.path.basename(self.dir) if self.dir else "YSCODE"))

    def update_status_bar(self):
        '''
        Update Status Bar
        '''
        self.statusBar().showMessage("%s | Line %d, Column %d" % (
            self.editor.path if self.editor.path else "Untitled",
            self.editor.textCursor().blockNumber() + 1,
            self.editor.textCursor().columnNumber() + 1))

    def show_info(self):
        '''
        Show Info
        '''
        QMessageBox.information(
            self, "About YSCODE", "YSCODE is a simple text editor.<br>Developed by Yusen Zheng.")

    def reset_fnd(self):
        '''
        Set Find mode to False
        '''
        self.fnd = False

    def fnd_before(self):
        '''
        Find the previous text
        '''
        if self.find_bar.text() != "":
            if not self.editor.find(self.find_bar.text(), QTextDocument.FindBackward):
                self.editor.moveCursor(QTextCursor.End)
                if self.editor.find(self.find_bar.text(), QTextDocument.FindBackward):
                    self.fnd = True
                else:
                    self.fnd = False
            else:
                self.fnd = True
        return self.fnd

    def fnd_next(self):
        '''
        Find the next text
        '''
        if self.find_bar.text() != "":
            if not self.editor.find(self.find_bar.text()):
                self.editor.moveCursor(QTextCursor.Start)
                if self.editor.find(self.find_bar.text()):
                    self.fnd = True
                else:
                    self.fnd = False
            else:
                self.fnd = True
        return self.fnd

    def rpl(self):
        '''
        Replace the text
        '''
        if self.find_bar.text() != "" and self.fnd:
            self.editor.textCursor().insertText(self.replace_bar.text())
        self.fnd_next()

    def rpl_all(self):
        '''
        Replace all the text
        '''
        if self.find_bar.text() != "":
            while self.fnd_next():
                self.editor.textCursor().insertText(self.replace_bar.text())

    def jump(self):
        '''
        Jump to the line
        '''
        if self.jump_bar.text() != "" and self.jump_bar.text().isdigit():
            self.editor.moveCursor(QTextCursor.Start)
            for _ in range(int(self.jump_bar.text()) - 1):
                self.editor.moveCursor(QTextCursor.Down)
            self.editor.moveCursor(QTextCursor.StartOfLine)

    def show_tree_menu(self, pos):
        '''
        Show Tree Menu
        '''
        index = self.tree.indexAt(pos)
        if not index.isValid():
            return
        if QFileInfo(self.model.filePath(index)).isDir():
            menu = QMenu()
            menu.addAction('Add File', lambda: self.add_file(index))
            menu.addAction('Add Folder', lambda: self.add_folder(index))
            menu.addAction('Move', lambda: self.move_file_or_folder(index))
            menu.addAction('Delete', lambda: self.delete_file_or_folder(index))
            menu.addAction('Rename', lambda: self.rename_file_or_folder(index))
            menu.exec_(self.tree.viewport().mapToGlobal(pos))
        else:
            menu = QMenu()
            menu.addAction('Move', lambda: self.move_file_or_folder(index))
            menu.addAction('Delete', lambda: self.delete_file_or_folder(index))
            menu.addAction('Rename', lambda: self.rename_file_or_folder(index))
            menu.exec_(self.tree.viewport().mapToGlobal(pos))

    def add_file(self, index):
        '''
        Add File in Tree Menu
        '''
        file_name, ok_pressed = QInputDialog.getText(
            self, "Create File", "File name:", QLineEdit.Normal, "")
        if ok_pressed and file_name != '':
            dir_path = self.model.filePath(index)
            file_path = os.path.join(dir_path, file_name)
            if os.path.exists(file_path):
                QMessageBox.warning(
                    self, 'Warning', 'Name already exists!', QMessageBox.Ok)
            else:
                with open(file_path, 'w') as f:
                    pass

    def add_folder(self, index):
        '''
        Add Folder in Tree Menu
        '''
        folder_name, ok_pressed = QInputDialog.getText(
            self, "Create Folder", "Folder name:", QLineEdit.Normal, "")
        if ok_pressed and folder_name != '':
            dir_path = self.model.filePath(index)
            folder_path = os.path.join(dir_path, folder_name)
            try:
                os.mkdir(folder_path)
            except OSError:
                QMessageBox.warning(
                    self, 'Warning', 'Name already exists!', QMessageBox.Ok)

    def move_file_or_folder(self, index):
        '''
        Move File or Folder in Tree Menu
        '''
        dir_path = QFileDialog.getExistingDirectory(self, 'Open Folder')
        if dir_path:
            file_path = self.model.filePath(index)
            file_name = os.path.basename(file_path)
            new_file_path = os.path.join(dir_path, file_name)
            if os.path.exists(new_file_path):
                QMessageBox.warning(
                    self, 'Warning', 'Name already exists!', QMessageBox.Ok)
            else:
                shutil.move(file_path, new_file_path)

    def delete_file_or_folder(self, index):
        '''
        Delete File or Folder in Tree Menu
        '''
        reply = QMessageBox.question(
            self, 'Delete', 'Are you sure to delete the selected file/folder?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.model.remove(index)

    def rename_file_or_folder(self, index):
        '''
        Rename File or Folder in Tree Menu
        '''
        file_path = self.model.filePath(index)
        is_folder = QFileInfo(file_path).isDir()
        fn = os.path.basename(file_path)
        fp = os.path.dirname(file_path)
        new_file_name, ok_pressed = QInputDialog.getText(
            self, "Rename", "New name:", QLineEdit.Normal, QDir.toNativeSeparators(fn))
        if ok_pressed and new_file_name:
            new_file_path = os.path.join(fp, new_file_name)
            new_file_path = QDir.toNativeSeparators(new_file_path)
            new_file_path = os.path.join(
                os.path.dirname(file_path), new_file_path)
            try:
                if is_folder:
                    os.rename(file_path, new_file_path)
                else:
                    shutil.move(file_path, new_file_path)
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Failed to rename: {e}")

    def toggle_sidebar(self):
        '''
        Display or hide the sidebar
        '''
        if self.tree.isVisible():
            self.tree.hide()
        else:
            self.tree.show()

    def toggle_terminal(self):
        '''
        Display or hide the terminal
        '''
        if self.terminal.isVisible():
            self.terminal.hide()
        else:
            self.terminal.show()
