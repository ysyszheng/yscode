'''
Highlighting for python code
Modified from the original code by Axel Erfurt
Edited by: Yusen Zheng
Fixed some bugs and added some features
'''

import ast
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QSyntaxHighlighter
from utils.utils import format


STYLES = {
    'keyword': format('#BB7FD7'),
    'operator': format('#6EB4C0'),
    'brace': format('#C79A6D'),
    'variable': format('#D17277'),
    'functions': format('#72AEE9'),
    'magicmethods': format('#6EB4BF'),
    'classes': format('#DABC81'),
    'string': format('#A1C181'),
    'triplestring': format('#A1C181'),
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
        'None', 'True', 'False', 'as', 'with', 'async', 'await',
    ]

    operators = [
        '=',
        '==', '!=', '<', '<=', '>', '>=',
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        '\+=', '-=', '\*=', '/=', '\%=',
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        tri = ("'''")
        trid = ('"""')

        self.tri_single = (QRegExp(tri), 1, STYLES['triplestring'])
        self.tri_double = (QRegExp(trid), 2, STYLES['triplestring'])

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

            # Variable names
            (r'\b(\w+)\b\s*(?=\=)', 1, STYLES['variable']),

            # Function names
            (r'\b(\w+)\b\s*(\()', 1, STYLES['functions']),

            # Class names
            (r'\bclass\b\s*(\w+)', 1, STYLES['classes']),

            # Magic methods
            (r'\b__(\w+)__\b', 0, STYLES['magicmethods']),

            # Single line comment
            (r'#[^\n]*', 0, STYLES['comment']),

            # Single-quoted string, possibly containing escape sequences
            (r"'(?:\\.|[^'\\])*'", 0, STYLES['string']),
            
            # Double-quoted string, possibly containing escape sequences
            (r'"(?:\\.|[^"\\])*"', 0, STYLES['string']),
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

    def in_quotes(self, text, position, delimiter):
        '''
        Check if the position is inside quotes
        '''
        in_quotes = False
        quote_delimiters = ['"', "'"]
        for quote in quote_delimiters:
            quote_start = text.find(quote, 0, position)
            quote_end = text.find(quote, position + delimiter.matchedLength())
            if quote_start >= 0 and quote_end >= 0 and quote_start < position < quote_end:
                in_quotes = True
                break
        return in_quotes

    def match_multiline(self, text, delimiter, in_state, style):
        '''
        Do highlighting of multi-line strings.
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
            # Check if the delimiter is inside quotes
            if self.in_quotes(text, start, delimiter):
                # Move past this match and continue searching
                start = delimiter.indexIn(text, start + add)
                continue
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
