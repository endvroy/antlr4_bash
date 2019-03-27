lexer grammar BashLexer;



PROGNAME : [-a-zA-Z0-9_./]+ ;
EQ : '=' -> pushMode(ASSIGN_RLS);
BLANK : [ \t]+ -> skip, pushMode(ARGS);
SQUOTE_STR : '\'' (~['\\] | '\\' [\\'])* '\'' ;
DQUOTE : '"' -> pushMode(INSIDE_DQUOTE);

mode ASSIGN_RLS;
LITERAL: [-a-zA-Z0-9_./=+];
BLANK_RLS: BLANK -> popMode;
//todo: add other cases

mode ARGS;
ARG: [-a-zA-Z0-9_=+./,]+;
ARG_SQUOTE_STR : SQUOTE_STR;
DOLLAR : '$' -> pushMode(VARNAME_IN_DQUOTE);
DOLLAR_LPAREN : '$(' -> pushMode(INSIDE_CST_DOLLAR);
BACKTICK : '`' -> pushMode(INSIDE_CST_BT);
ARG_DQUOTE : DQUOTE -> pushMode(INSIDE_DQUOTE);
ARGS_BLANK : [ \t]+ -> skip;
PIPE : '|' -> popMode;

mode INSIDE_DQUOTE;
DQUOTE_CONTENT : (~["\\$] | '\\' [\\"])+ ;
DQUOTE_DOLLAR : '$' -> type(DOLLAR), pushMode(VARNAME_IN_DQUOTE);
DQUOTE_DOLLAR_LPAREN : '$(' -> type(DOLLAR_LPAREN), pushMode(INSIDE_CST_DOLLAR);
DQUOTE_BACKTICK : '`' -> type(BACKTICK), pushMode(INSIDE_CST_BT);
TAIL_DQUOTE : DQUOTE -> type(DQUOTE), popMode;

mode INSIDE_CST_DOLLAR;
// todo: delegate to entry?
CST_CONTENT : PROGNAME -> type(PROGNAME);
CST_BLANK : BLANK -> type(BLANK);
RPAREN : ')' -> popMode;

mode INSIDE_CST_BT;
CST_CONTENT_BT : PROGNAME -> type(PROGNAME);
CST_BLANK_BT : BLANK -> type(BLANK);
TAIL_BACKTICK : '`' -> popMode ;

mode VARNAME_IN_DQUOTE;
VARNAME : ( [$!] | [a-zA-Z0-9_]+) -> popMode;

