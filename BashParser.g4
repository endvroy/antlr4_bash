parser grammar BashParser;

options {tokenVocab=BashLexer;}

pipeline : pipeline PIPE cmd
| cmd;

cmd : (assign_list RLS_BLANK)? exec | assign_list;

assign_list : assign_list RLS_BLANK assign
| assign;

assign: PROGNAME EQ assign_rls;

assign_rls : (LITERAL | RLS_SQUOTE_STR | RLS_VAR | dquote_str | subst)*;

exec: PROGNAME arg_list? ARGS_BLANK?;

arg_list : arg_list ARGS_BLANK arg
| arg
;

arg: (ARG | SQUOTE_STR | VAR | dquote_str | subst)+;

dquote_str : DQUOTE (DQUOTE_CONTENT | VAR | subst)* DQUOTE;

subst : cst | lpst | rpst;

cst : DOLLAR_LPAREN pipeline? RPAREN
| BACKTICK pipeline? BACKTICK
;

lpst : LT_LPAREN pipeline? RPAREN;

rpst : GT_LPAREN pipeline? RPAREN;
