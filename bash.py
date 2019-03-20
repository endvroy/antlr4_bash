import ply.lex as lex
import ply.yacc as yacc
from pprint import pprint
from bashlex.ast import node as AST

tokens = (
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
    'DOLLAR',
    'BTICK',
    'COMMA',
    'FSLASH',
    'SQUOTE_STR',
    'VARNAME',
    'FPATH',
    'ARGCHARS'
    # 'ANYCHAR'
)

# t_VARNAME = r'[a-zA-Z0-9_]+'
# t_FPATH = r'(/[\w-_.]+)+'
# t_ARGCHARS=r'[-+=_.,/]'

t_SQUOTE_STR = r"\$?'([^'\\]|\\.)*'"
t_WORD = r'[a-zA-Z0-9_][-a-zA-Z0-9_]*'
t_NUM = r'[0-9]+'
# t_LTLTMINUS = r'<<-'
t_LTLT = r'<<'
# t_LTGT = r'<>'
t_LTAND = r'<&'
t_LT = r'<'
t_GTGT = r'>>'
t_GTAND = r'>&'
# t_GTPIPE = r'>\|'
t_GT = r'>'
t_ANDAND = r'&&'
t_ANDGT = r'&>'
t_AND = r'&'
t_PIPEPIPE = '\|\|'
t_PIPE = '\|'
# t_SEMISEMI = r';;'
# t_SEMI = r';'
t_MINUS = r'-'
t_PLUS = r'\+'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_UNDERSCORE = r'_'
# t_SQUOTE = r"'"
t_DQUOTE = r'"'
t_EQ = r'='
# t_BANG = r'!'
t_BLANK = r'[\t ]+'
t_DOT = r'\.'
t_DOLLAR = r'\$'
t_BTICK = r'`'
t_COMMA = r','
t_FSLASH = r'/'
# t_ANYCHAR = r'.'
# t_ignore = ' \t'

lexer = lex.lex()


# todo: add squote str and dquote str

def p_pipeline(t):
    """
    pipeline : pipeline PIPE cmd
    | cmd
    """
    if len(t) == 4:
        t[0] = AST(kind='pipeline', prev=t[1], cmd=t[3])
    else:
        t[0] = t[1]


def p_cmd(t):
    """
    cmd : opt_blank prog BLANK arg_list opt_blank
    | opt_blank prog opt_blank
    """
    if len(t) == 6:
        t[0] = AST(kind='cmd', prog=t[2], args=t[4])
    else:
        t[0] = AST(kind='cmd', prog=t[2])


def p_cst(t):
    # command substitutions
    """
    cst : DOLLAR LPAREN cmd RPAREN
    | BTICK cmd BTICK
    """
    if len(t) == 5:
        t[0] = AST(kind='cst', cmd=t[3])
    else:
        t[0] = AST(kind='cst', cmd=t[2])


def p_pst(t):
    """
    pst : pst_left
    | pst_right
    """
    t[0] = t[1]


def p_pst_left(t):
    # process substitutions
    """
    pst_left : LT LPAREN cmd RPAREN
    """
    t[0] = AST(kind='pst_left', cmd=t[3])


def p_pst_right(t):
    # process substitutions
    """
    pst_right : GT LPAREN cmd RPAREN
    """
    t[0] = AST(kind='pst_right', cmd=t[3])


def p_opt_blank(t):
    """
    opt_blank : BLANK
    |
    """


def p_prog(t):
    """
    prog : progword
    | cst
    """
    t[0] = AST(kind='prog', name=t[1])


def p_progword(t):
    """
    progword : progword progpart
    | progpart
    """
    if len(t) == 3:
        t[0] = t[1] + t[2]
    else:
        t[0] = t[1]


def p_progpart(t):
    """
    progpart : WORD
    | NUM
    | MINUS
    | UNDERSCORE
    | DOT
    | FSLASH
    """
    t[0] = t[1]


def p_arg_list(t):
    """
    arg_list : arg_list BLANK arg
    | arg
    """
    if len(t) == 4:
        t[0] = t[1] + [t[3]]
    else:
        t[0] = [t[1]]


def p_arg(t):
    """
    arg : argword
    | cst
    | pst
    | var
    """
    t[0] = AST(kind='arg', value=t[1])


def p_argword(t):
    """
    argword : argword argpart
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
    | COMMA
    | FSLASH
    | SQUOTE_STR
    """
    t[0] = t[1]


def p_var(t):
    """
    var : DOLLAR WORD
    """
    t[0] = AST(kind='var', name=t[2])


def p_dquote_str(t):
    """
    dquote_str : DQUOTE dquote_content DQUOTE
    """
    return AST(kind='squote_str', content=t[2])


def p_dquote_content(t):
    """
    dquote_content : dquote_content dquote_part
    |
    """
    if len(t) == 3:
        t[0] = t[1] + t[2]
    else:
        t[0] = ''


def p_dquote_part(t):
    """
    dquote_part : cst
    | WORD
    | NUM
    | PLUS
    | MINUS
    | EQ
    | UNDERSCORE
    | DOT
    | COMMA
    | FSLASH
    | SQUOTE_STR
    | BLANK
    """


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
    # print(tokens)
    result = parser.parse(s)
    # pprint(result)
    print(result.dump())
