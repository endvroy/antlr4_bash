from antlr4 import *
# from .gen.BashLexer import BashLexer
from .gen.BashParser import BashParser
from .BashASTVisitor import BashASTVisitor
from .prof_loader import PanicBashLexer


def raw_parse(line):
    input_stream = InputStream(line)
    lexer = PanicBashLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BashParser(stream)
    parser._errHandler = BailErrorStrategy()
    tree = parser.pipeline()
    return tree


def get_ast(tree):
    visitor = BashASTVisitor()
    ast = visitor.visit(tree)
    return ast


def parse(line):
    tree = raw_parse(line)
    visitor = BashASTVisitor()
    ast = visitor.visit(tree)
    return ast


if __name__ == '__main__':
    l = input('input:\n')
    tree = parse(l)
    visitor = BashASTVisitor()
    ast = visitor.visit(tree)
