parser grammar BashParser;

options {tokenVocab=BashLexer;}

pipeline : pipeline PIPE cmd
| cmd;

cmd : assign* exec | assign;

assign: PROGNAME EQ (LITERAL | RLS_SQUOTE_STR | RLS_VAR | dquote_str | cst)* RLS_BLANK;

exec: PROGNAME arg_list? ARGS_BLANK?;

arg_list : arg_list ARGS_BLANK arg
| arg
;

arg: (ARG | SQUOTE_STR | VAR | dquote_str | cst)+;

dquote_str : DQUOTE (DQUOTE_CONTENT | VAR | cst)* DQUOTE;

cst : DOLLAR_LPAREN pipeline? RPAREN
| BACKTICK pipeline? BACKTICK
;
