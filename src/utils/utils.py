'''
Utility variables and functions.
'''

import sys

welcome_text = \
    r'                          _       ' + '\n' + \
    r'                         | |      ' + '\n' + \
    r'  _   _ ___  ___ ___   __| | ___  ' + '\n' + \
    r' | | | / __|/ __/ _ \ / _` |/ _ \ ' + '\n' + \
    r' | |_| \__ \ (_| (_) | (_| |  __/ ' + '\n' + \
    r'  \__, |___/\___\___/ \__,_|\___| ' + '\n' + \
    r'   __/ |                          ' + '\n' + \
    r'  |___/                           ' + '\n'


def log(msg):
    '''
    Display the message with the file name and line number of the caller.
    '''
    fn = sys._getframe().f_back.f_code.co_filename
    ln = sys._getframe().f_back.f_lineno
    print('File \"%s\", line %d, Msg:' % (fn, ln), msg)
