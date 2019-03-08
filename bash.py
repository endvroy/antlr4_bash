import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'LETTER',
    'DIGIT',
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
    # t_MINUS,
    'LCURLY',
    'RCURLY',
    'LPAREN',
    'RPAREN',
    'UNDERSCORE',
    'SQUOTE',
    'DQUOTE',
    'EQUAL',
    'BANG',
    # t_BLANK,
    'ANYWORD'
)

t_LETTER = r'[a-zA-Z]'
t_DIGIT = r'[0-9]'
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
# t_MINUS = r'-'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_UNDERSCORE = r'_'
t_SQUOTE = r"'"
t_DQUOTE = r'"'
t_EQUAL = r'='
t_BANG = r'!'
# t_BLANK = r'[\t ]+'
t_ANYWORD = r'.+'
t_ignore = ' \t'

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

def p_word(t):
    """
    word : LETTER
    | word LETTER
    | word UNDERSCORE
    """


def p_cmd(t):
    """
    cmd : prog arg_list
    """


def p_prog(t):
    """
    prog : word
    """


def p_arg_list(t):
    """
    arg_list : arg arg_list
    |
    """


def p_arg(t):
    # todo: consider flags
    # todo: consider substitutions
    """
    arg : word
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
    print(tokens)
    parser.parse(s)
