lexer grammar BashLexer;



PROGNAME : [-a-zA-Z0-9_./]+ ;
EQ : '=' -> pushMode(ASSIGN_RLS);
BLANK : [ \t]+ -> skip, pushMode(ARGS);
SQUOTE_STR : '\'' (~['\\] | '\\' [\\'])* '\'' ;
DQUOTE : '"' -> pushMode(INSIDE_DQUOTE);

mode ASSIGN_RLS;
BLANK_RLS: BLANK -> popMode;
//todo: add other cases

mode ARGS;
ARG: [-a-zA-Z0-9_=+./,]+;
DOLLAR_LPAREN : '$(' -> pushMode(INSIDE_CST_DOLLAR);
BACKTICK : '`' -> pushMode(INSIDE_CST_BT);
DOLLAR : '$' -> pushMode(VARNAME_IN_DQUOTE);
ARGS_BLANK : [ \t]+ -> skip;
PIPE : '|' -> popMode;

mode INSIDE_DQUOTE;
DQUOTE_DOLLAR_LPAREN : '$(' -> type(DOLLAR_LPAREN), pushMode(INSIDE_CST_DOLLAR);
DQUOTE_BACKTICK : '`' -> type(BACKTICK), pushMode(INSIDE_CST_BT);
DQUOTE_DOLLAR : '$' -> type(DOLLAR), pushMode(VARNAME_IN_DQUOTE);
DQUOTE_CONTENT : (~["\\] | '\\' [\\"])+? ;
TAIL_DQUOTE : DQUOTE -> type(DQUOTE), popMode;

mode INSIDE_CST_DOLLAR;
// todo: delegate to entry?
RPAREN : ')' -> popMode;
CST_BLANK : BLANK -> type(BLANK);
CST_CONTENT : PROGNAME -> type(PROGNAME);

mode INSIDE_CST_BT;
TAIL_BACKTICK : '`' -> popMode ;
CST_BLANK_BT : BLANK -> type(BLANK);
CST_CONTENT_BT : PROGNAME -> type(PROGNAME);

mode VARNAME_IN_DQUOTE;
VARNAME : ( [$!] | [a-zA-Z0-9_]+) -> popMode;

