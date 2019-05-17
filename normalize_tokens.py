from antlr4 import *
from .gen.BashParser import BashParser
from .BashASTVisitor import BashASTVisitor
import itertools
from .prof_loader import PanicBashLexer
from bashlint.bash import argument_types


def parse(line):
    input_stream = InputStream(line)
    lexer = PanicBashLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = BashParser(stream)
    parser._errHandler = BailErrorStrategy()
    tree = parser.pipeline()
    return tree


def get_normalize_tokens(ast):
    if ast == []:
        return []
    if ast.kind.isupper():
        # leaf node
        if ast.kind == 'VAR':
            # var node
            # append $
            return ['$'] + [ast.value[1:]]
        else:
            # return the lexeme as-is
            return [ast.value]
    elif ast.kind == 'pipeline':
        if ast.prev is None:
            prev_tokens = []
        else:
            prev_tokens = get_normalize_tokens(ast.prev)
            prev_tokens.append('|')
        return prev_tokens + get_normalize_tokens(ast.last_cmd)
    elif ast.kind == 'cmd':
        assign_list_tokens = get_sstl(ast.assign_list, get_normalize_tokens)
        prog_tokens = get_normalize_tokens(ast.prog)
        args_tokens = get_sstl(ast.args, get_normalize_tokens)
        redir_tokens = get_sstl(ast.redir, get_normalize_tokens)
        if assign_list_tokens:
            assign_list_tokens.append(' ')
        if args_tokens:
            args_tokens.insert(0, ' ')
        if redir_tokens:
            redir_tokens.insert(0, ' ')
        tokens = assign_list_tokens + prog_tokens + args_tokens + redir_tokens
        return tokens
    elif ast.kind == 'assign':
        lhs = [ast.lhs]
        rhs = get_normalize_tokens(ast.rhs)
        return lhs + ['='] + rhs
    elif ast.kind == 'assign_rhs':
        return list(itertools.chain.from_iterable(get_normalize_tokens(x) for x in ast.parts))
    elif ast.kind == 'redir':
        lhs = []
        if ast.lhs:
            lhs.append(ast.lhs)
        rhs = get_normalize_tokens(ast.rhs)
        return lhs + [ast.type] + rhs
    elif ast.kind == 'prog':
        return list(itertools.chain.from_iterable(get_normalize_tokens(x) for x in ast.parts))
    elif ast.kind == 'arg':
        return list(itertools.chain.from_iterable(get_normalize_tokens(x) for x in ast.parts))
    elif ast.kind in argument_types:
        return list(itertools.chain.from_iterable(get_normalize_tokens(x) for x in ast.parts))
    elif ast.kind == 'flag':
        tokens = [ast.name]
        if ast.value is not None:
            tokens.append(' ')
            tokens.extend(itertools.chain.from_iterable(
                get_normalize_tokens(x) for x in ast.value))
        return tokens
    elif ast.kind == 'cst':
        return ['$('] + get_normalize_tokens(ast.pipeline) + [')']
    elif ast.kind == 'lpst':
        return ['<('] + get_normalize_tokens(ast.pipeline) + [')']
    elif ast.kind == 'rpst':
        return ['>('] + get_normalize_tokens(ast.pipeline) + [')']
    elif ast.kind == 'arith_subst':
        return ['$(('] + get_normalize_tokens(ast.pipeline) + ['))']
    elif ast.kind == 'param_exp':
        return ['${'] + list(itertools.chain.from_iterable(get_normalize_tokens(x) for x in ast.parts)) + ['}']
    elif ast.kind == 'dquote_str':
        return ['"'] + list(itertools.chain.from_iterable(get_normalize_tokens(x) for x in ast.parts)) + ['"']
    elif ast.kind == 'squote_str':
        return ["'"] + list(itertools.chain.from_iterable(get_normalize_tokens(x) for x in ast.parts)) + ["'"]
    elif ast.kind == 'paren_grp':
        return ['('] + get_normalize_tokens(ast.pipeline) + [')']
    elif ast.kind == 'curly_grp':
        return ['{', ' '] + get_normalize_tokens(ast.pipeline) + ['}']


def get_sstl(l, f):
    """space-separated token list"""
    token_list = []
    for node in l:
        if token_list:
            token_list.append(' ')
        token = f(node)
        token_list.extend(token)
    return token_list


def normalize_line(line):
    parse_tree = parse(line)
    visitor = BashASTVisitor()
    ast = visitor.visit(parse_tree)
    tokens = get_normalize_tokens(ast)
    return tokens


if __name__ == '__main__':
    l = input('input:\n')
    tokens = normalize_line(l)
    print(''.join(tokens))
