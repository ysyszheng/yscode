'''mode: 0 - noraml, 1 - insert, 2 - visual, 3 - replace, 4 - command'''

class Mode:
    def __init__(self, init_mode=0):
        self.mode = init_mode
        self.mode_list = ['NORMAL', 'INSERT', 'VISUAL', 'REPLACE', 'COMMAND']
    
    def __str__(self):
        return self.mode_list[self.mode]
    
    def __repr__(self):
        return self.mode_list[self.mode]
    
    def __eq__(self, mode):
        return self.mode == mode
    
    def __ne__(self, mode):
        return self.mode != mode
    
    def __lt__(self, mode):
        return self.mode < mode
    
    def __gt__(self, mode):
        return self.mode > mode
    
    def __le__(self, mode):
        return self.mode <= mode
    
    def __ge__(self, mode):
        return self.mode >= mode

    def get_mode(self):
        return self.mode

    def get_mode_name(self):
        return self.mode_list[self.mode]
    
    def set_mode(self, mode):
        self.mode = mode

    def is_mode(self, mode):
        return self.mode == mode
    