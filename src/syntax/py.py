'''
Highlighting for python code
Modified from the original code by Axel Erfurt
Edited by: Yusen Zheng
Fixed some bugs and added some features
'''

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


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


STYLES = {
    'keyword': format('#BB7FD7'),
    'operator': format('#6EB4C0'),
    'brace': format('#C79A6D'),
    'variable': format('#D17277'),
    'functions': format('#72AEE9'),
    'magicmethods': format('#6EB4BF'),
    'classes': format('#DABC81'),
    'string': format('#A1C181'),
    'string2': format('#A1C181'),
    'comment': format('#80838D', 'italic'),
    'self': format('#DABC81', 'italic'),
    'numbers': format('#C0956A'),
}


class Highlighter(QSyntaxHighlighter):
    '''
    Syntax highlighter for the Python language.
    '''
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'super', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        tri = ("'''")
        trid = ('"""')
        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp(tri), 1, STYLES['string2'])
        self.tri_double = (QRegExp(trid), 2, STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in Highlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in Highlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in Highlighter.braces]

        # All other rules
        rules += [
            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b',
             0, STYLES['numbers']),

            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # Double-quoted string, possibly containing escape sequences ### "\"([^\"]*)\"" ### "\"(\\w)*\""
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # variable names
            (r'\b(\w+)\b\s*(?=\=)', 1, STYLES['variable']),

            # function names, followed by an ()
            (r'\b(\w+)\b\s*(\()', 1, STYLES['functions']),

            # class names
            (r'\bclass\b\s*(\w+)', 1, STYLES['classes']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),

            # Magic methods
            (r'\b__(\w+)__\b', 0, STYLES['magicmethods']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        '''
        Apply syntax highlighting to the given block of text.
        '''
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        '''
        Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        '''
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
