from antlr4 import *
from BashLexer import BashLexer
from BashParser import BashParser
from io import StringIO

if __name__ == '__main__':
    l = input('$ ')
    # f = StringIO(l)
    input_stream = InputStream(l)
    lexer = BashLexer(input_stream)
    stream = CommonTokenStream(lexer)
    # stream.fill()
    # tokens = stream.tokens
    parser = BashParser(stream)
    tree = parser.cmd()
