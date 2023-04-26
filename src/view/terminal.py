from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
import subprocess

class Terminal(QWidget):
    def __init__(self):
        super().__init__()
        self.command_input = QLineEdit()
        self.output_text = QTextEdit()

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
        self.command_input.setPlaceholderText("Enter command here...")
        self.output_text.setReadOnly(True)

    def run_command(self):
        command = self.command_input.text()
        self.output_text.setText("Working...")

        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            output = result.stdout + result.stderr
        except subprocess.CalledProcessError as e:
            output = e.stderr

        self.output_text.setText(output)

if __name__ == "__main__":
    app = QApplication([])
    terminal = Terminal()
    terminal.show()
    app.exec_()