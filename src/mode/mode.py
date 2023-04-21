# mode: 0 - noraml, 1 - insert, 2 - visual, 3 - command
mode_list = ['normal', 'insert', 'visual', 'command']

class Mode:
    def __init__(self):
        self.mode = 0

    def get_mode(self):
        return self.mode
    
    def set_mode(self, mode):
        self.mode = mode
