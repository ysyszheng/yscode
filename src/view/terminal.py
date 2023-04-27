'''
Simulate a terminal in a widget
'''

import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import QProcess


class Terminal(QWidget):
    '''
    Simulate terminal class
    '''

    def __init__(self):
        super().__init__()
        self.command_input = QLineEdit()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.current_directory = os.path.expanduser('~')

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.command_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.output_text)

        char_width = self.fontMetrics().averageCharWidth()
        main_layout.setContentsMargins(0, char_width, char_width, char_width)

        self.setLayout(main_layout)
        self.initUI()

        self.command_input.returnPressed.connect(self.run_command)

    def initUI(self):
        '''
        Initialize UI
        '''
        font = QFont("Consolas", 12)
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.command_input.setFont(font)
        self.output_text.setFont(font)
        self.output_text.setLineWrapMode(QTextEdit.NoWrap)
        self.command_input.setStyleSheet("background-color: rgb(29, 31, 35);\
            color: rgb(171, 177, 189);\
            border: 1px solid rgb(34, 37, 42);")
        self.output_text.setStyleSheet("background-color: rgb(29, 31, 35);\
            color: rgb(171, 177, 189);")
        self.command_input.setPlaceholderText(
            "Enter command here... (Press Enter to run)")
        self.output_text.setReadOnly(True)

    def run_command(self):
        '''
        Run command
        '''
        command = self.command_input.text()
        self.command_input.clear()
        if command == "clear":
            self.output_text.clear()
            return
        self.output_text.append(
            f'$ {os.path.basename(self.current_directory)}> {command}\n')

        if command.startswith('cd'):
            self.handle_cd(command)
        else:
            self.handle_command(command)

    def handle_cd(self, command):
        '''
        Handle change directory command
        '''
        try:
            os.chdir(command[3:])
            self.current_directory = os.getcwd()
        except FileNotFoundError:
            self.output_text.append(
                f'No such file or directory: {command[3:]}\n')
        except NotADirectoryError:
            self.output_text.append(f'Not a directory: {command[3:]}\n')
        except PermissionError:
            self.output_text.append(f'Permission denied: {command[3:]}\n')
        except:
            self.output_text.append(f'Error: {command[3:]}\n')
        finally:
            self.output_text.append(
                f'Current directory: {self.current_directory}\n')
        self.output_text.moveCursor(QTextCursor.End)

    def handle_command(self, command):
        '''
        Handle other command
        '''
        process = QProcess(self)
        if os.name == 'nt':
            process.setProgram('powershell')
            process.setArguments(['/c', command])
        else:
            process.setProgram('/bin/bash')
            process.setArguments(['-c', command])
        process.setWorkingDirectory(self.current_directory)
        process.readyReadStandardOutput.connect(
            lambda: self.handle_output(process))
        process.readyReadStandardError.connect(
            lambda: self.handle_output(process))
        process.finished.connect(lambda: process.deleteLater())
        process.start()

    def handle_output(self, process):
        '''
        Print output on text box
        '''
        data = process.readAllStandardOutput()
        data += process.readAllStandardError()
        output = str(data, encoding='utf-8')
        self.output_text.insertPlainText(output)
        self.output_text.moveCursor(QTextCursor.End)


if __name__ == "__main__":
    app = QApplication([])
    terminal = Terminal()
    terminal.show()
    app.exec_()
