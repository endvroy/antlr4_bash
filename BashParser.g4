parser grammar BashParser;

options {tokenVocab=BashLexer;}

cmd: PROGNAME arg_list? ARGS_BLANK?;

arg_list : arg_list ARGS_BLANK arg
| arg
;

arg: (ARG | SQUOTE_STR | VAR | dquote_str | cst)+;

dquote_str : DQUOTE (DQUOTE_CONTENT | VAR | cst)* DQUOTE;

cst : DOLLAR_LPAREN cmd? RPAREN
| BACKTICK cmd? BACKTICK
;
