import sys
import mimetypes

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
    fn = sys._getframe().f_back.f_code.co_filename
    ln = sys._getframe().f_back.f_lineno
    print('File \"%s\", line %d, Msg:' % (fn, ln), msg)
