from antlr4 import *
from gen.BashLexer import BashLexer

if __name__ == '__main__':
    l = input('$ ')
    input_stream = InputStream(l)
    lexer = BashLexer(input_stream)
    stream = CommonTokenStream(lexer)
    stream.fill()
    tokens = stream.tokens
    # parser = BashParser(stream)
    # tree = parser.cmd()
