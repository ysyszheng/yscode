'''
Utility variables and functions.
'''

import sys
from PyQt5.QtGui import QColor, QTextCharFormat, QFont

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


def format(color, style=''):
    '''
    Return a QTextCharFormat with the given attributes.
    '''
    _color = QColor()
    _color.setNamedColor(color)
    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    if 'italicbold' in style:
        _format.setFontItalic(True)
        _format.setFontWeight(QFont.Bold)
    return _format
