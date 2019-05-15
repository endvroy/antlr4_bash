from antlr4 import *
from .gen.BashLexer import BashLexer
from .gen.BashParser import BashParser
from contextlib import redirect_stderr
import sys


class PanicBashLexer(BashLexer):
    def recover(self, re: RecognitionException):
        raise re


CM_PATH = '/Users/ruoyi/Projects/PycharmProjects/data_fixer/bash/all.cm.filtered'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    err_lines = []
    with open(CM_PATH) as cm_f, redirect_stderr(sys.stdout):
        lines = cm_f.readlines()
        for i, line in enumerate(lines):
            try:
                input_stream = InputStream(line)
                lexer = PanicBashLexer(input_stream)
                stream = CommonTokenStream(lexer)
                parser = BashParser(stream)
                parser._errHandler = BailErrorStrategy()
                parser.pipeline()
            except:
                err_lines.append(i)
                print(bcolors.WARNING)
                print('from line {}'.format(i + 1))
                print(bcolors.ENDC)
                print('---------------')
    print('success rate: {:.3f}'.format((1 - len(err_lines) / len(lines)) * 100))


if __name__ == '__main__':
    main()
