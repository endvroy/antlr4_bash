from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy
from bash_parser.BashASTVisitor import BashASTVisitor
from bash_parser.gen.BashParser import BashParser
from bash_parser.normalize_tokens import get_normalize_tokens
from bash_parser.prof_loader import PanicBashLexer


def normalize_line(line):
    parse_tree = parse(line)
    visitor = BashASTVisitor()
    ast = visitor.visit(parse_tree)
    tokens = get_normalize_tokens(ast)
    return tokens


def parse(line):
    input_stream = InputStream(line)
    lexer = PanicBashLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BashParser(stream)
    parser._errHandler = BailErrorStrategy()
    tree = parser.pipeline()
    return tree
