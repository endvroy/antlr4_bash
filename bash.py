import ply.lex as lex
import ply.yacc as yacc
from pprint import pprint

tokens = (
    'ARGWORD',
    'WORD',
    'NUM',
    'LTLTMINUS',
    'LTLT',
    'LTGT',
    'LTAND',
    'LT',
    'GTGT',
    'GTAND',
    'GTPIPE',
    'GT',
    'ANDAND',
    'ANDGT',
    'AND',
    'PIPEPIPE',
    'PIPE',
    'SEMISEMI',
    'SEMI',
    'MINUS',
    'PLUS',
    'LCURLY',
    'RCURLY',
    'LPAREN',
    'RPAREN',
    'UNDERSCORE',
    'SQUOTE',
    'DQUOTE',
    'EQ',
    'BANG',
    'BLANK',
    'DOT',
    # 'ANYCHAR'
)

t_WORD = r'[a-zA-Z0-9_][-a-zA-Z0-9_]*'
t_NUM = r'[0-9]+'
t_LTLTMINUS = r'<<-'
t_LTLT = r'<<'
t_LTGT = r'<>'
t_LTAND = r'<&'
t_LT = r'<'
t_GTGT = r'>>'
t_GTAND = r'>&'
t_GTPIPE = r'>\|'
t_GT = r'>'
t_ANDAND = r'&&'
t_ANDGT = r'&>'
t_AND = r'&'
t_PIPEPIPE = '\|\|'
t_PIPE = '\|'
t_SEMISEMI = r';;'
t_SEMI = r';'
t_MINUS = r'-'
t_PLUS = r'\+'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_UNDERSCORE = r'_'
t_SQUOTE = r"'"
t_DQUOTE = r'"'
t_EQ = r'='
t_BANG = r'!'
t_BLANK = r'[\t ]+'
t_DOT = r'\.'
# t_ANYCHAR = r'.'
# t_ignore = ' \t'

lexer = lex.lex()


# def p_flags():
#     """
#     flag : LONG_FLAG_HEAD ident
#     | FLAG_HEAD ident
#     | ident EQ more_ident
#     """

# def p_ident(t):
#     """
#
#     :param t:
#     :return:
#     """

# def t_opt_blank(t):
#     """
#     opt_blank : BLANK
#     |
#     """


def p_cmd(t):
    """
    cmd : prog BLANK arg_list
    | prog
    """
    if len(t) == 4:
        t[0] = [t[1]]
        t[0].append(t[3])
    else:
        t[0] = [t[1]]


def p_prog(t):
    """
    prog : WORD
    """
    t[0] = t[1]


def p_arg_list(t):
    """
    arg_list : arg BLANK arg_list
    | arg
    """
    if len(t) == 4:
        t[0] = [t[1]] + t[3]
    else:
        t[0] = [t[1]]


def p_arg(t):
    # todo: consider substitutions
    """
    arg : argword
    """
    t[0] = t[1]


def p_argword(t):
    """
    argword : argpart argword
    | argpart
    """
    if len(t) == 3:
        t[0] = t[1] + t[2]
    else:
        t[0] = t[1]


def p_argpart(t):
    """
    argpart : WORD
    | NUM
    | PLUS
    | MINUS
    | EQ
    | UNDERSCORE
    | DOT
    """
    t[0] = t[1]


parser = yacc.yacc()

if __name__ == '__main__':
    s = input('$ ')
    lexer.input(s)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        tokens.append(tok)
    print(tokens)
    result = parser.parse(s, debug=True)
    pprint(result)
