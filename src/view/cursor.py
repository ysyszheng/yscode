'''Set Cursor style for different modes'''
from PyQt5.QtGui import QTextCursor
from mode.mode import Mode

class Cursor(QTextCursor):
    def __init__(self, document):
        super().__init__(document)
        self.mode = Mode()
        self.update_cursor_style()

    def __call__(self):
        return self

    def set_mode(self, mode):
        self.mode.set_mode(mode)
        self.update_cursor_style()

    def update_cursor_style(self):
        if self.mode == 0:          # normal mode
            self.normal_mode()
        elif self.mode == 1:        # insert mode
            self.insert_mode()
        elif self.mode == 2:        # visual mode
            self.visual_mode()
        elif self.mode == 3:        # repalce mode
            self.replace_mode()
        elif self.mode == 4:        # command mode
            self.command_mode()
        else:
            raise Exception('Invalid mode')
    
    def normal_mode(self):
        pass

    def insert_mode(self):
        pass
    
    def visual_mode(self):
        pass

    def replace_mode(self):
        pass

    def command_mode(self):
        pass

    def moveLeft(self):
        self.movePosition(9)

    def moveRight(self):
        self.movePosition(19)

    def moveUp(self):
        self.movePosition(2)

    def moveDown(self):
        self.movePosition(12)