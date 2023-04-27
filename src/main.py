'''
Entry point of the application.
'''

import sys
from view.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("YSCODE")
    window = MainWindow()
    window.show()
    window.showMaximized()
    app.exec_()
