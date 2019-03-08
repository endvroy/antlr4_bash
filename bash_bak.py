tokens = ("LETTER",
          "DIGIT",
          "LTLTMINUS",
          "LTLT",
          "LTGT",
          "LTAND",
          "LT",
          "GTGT",
          "GTAND",
          "GTPIPE",
          "GT",
          "ANDAND",
          "ANDGT",
          "AND",
          "PIPEPIPE",
          "PIPE",
          "SEMISEMI",
          "SEMI",
          "TIME",
          "MINUS",
          "LCURLY",
          "RCURLY",
          "LPAREN",
          "RPAREN",
          "UNDERSCORE",
          "EQUAL",
          "BANG",
          "NL",)

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
t_TIME = r'-p'
t_MINUS = r'-'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_UNDERSCORE = r'_'
t_EQUAL = r'='
t_BANG = r'!'
t_NL = r'\n'
