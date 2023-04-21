import sys
from view.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("MEOW Editor")
    window = MainWindow()
    window.show()
    app.exec_()
