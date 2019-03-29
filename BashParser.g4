parser grammar BashParser;

options {tokenVocab=BashLexer;}

entry : assign* cmd | assign;

assign: PROGNAME EQ (LITERAL | RLS_SQUOTE_STR | RLS_VAR | dquote_str | cst)* RLS_BLANK;

cmd: PROGNAME arg_list? ARGS_BLANK?;

arg_list : arg_list ARGS_BLANK arg
| arg
;

arg: (ARG | SQUOTE_STR | VAR | dquote_str | cst)+;

dquote_str : DQUOTE (DQUOTE_CONTENT | VAR | cst)* DQUOTE;

cst : DOLLAR_LPAREN cmd? RPAREN
| BACKTICK cmd? BACKTICK
;
