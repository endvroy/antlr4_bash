lexer grammar BashLexer;

PROGNAME : [-a-zA-Z0-9_./]+ -> mode(NECK);
BLANK : [ \t]+ -> skip;
RPAREN : ')' -> popMode;

mode NECK;
NECK_BLANK : BLANK -> skip, mode(ARGS);
EQ : '=' -> mode(ASSIGN_RLS);
END : ('\n' | EOF | RPAREN) -> popMode;

mode ARGS;
ARG: (~[$<>`()|'" \t])+;
SQUOTE_STR : '\'' (~['\\] | '\\' [\\'])* '\'' ;
VAR : '$' ( [$!] | [a-zA-Z0-9_]+)?;
DOLLAR_LPAREN : '$(' -> pushMode(DEFAULT_MODE);
BACKTICK : '`' -> pushMode(INSIDE_CST_BT);
DQUOTE : '"' -> pushMode(INSIDE_DQUOTE);
ARGS_BLANK : BLANK;
PIPE : '|' -> mode(DEFAULT_MODE);
ARGS_END: RPAREN -> popMode;

mode ASSIGN_RLS;
LITERAL: (~[$<>`()|'" \t])+;
RLS_SQUOTE_STR : SQUOTE_STR ;
RLS_VAR : '$' ( [$!] | [a-zA-Z0-9_]+)?;
RLS_DOLLAR_LPAREN : '$(' -> pushMode(DEFAULT_MODE);
RLS_BACKTICK : '`' -> pushMode(INSIDE_CST_BT);
RLS_DQUOTE : '"' -> pushMode(INSIDE_DQUOTE);
RLS_BLANK: BLANK -> mode(DEFAULT_MODE);
RLS_END: RPAREN -> popMode;
// todo: add other cases

mode INSIDE_DQUOTE;
DQUOTE_CONTENT : (~["\\$] | '\\' [\\"])+;
DQUOTE_VAR : VAR;
DQUOTE_DOLLAR_LPAREN : '$(' -> type(DOLLAR_LPAREN), pushMode(DEFAULT_MODE);
DQUOTE_BACKTICK : '`' -> type(BACKTICK), pushMode(INSIDE_CST_BT);
TAIL_DQUOTE : DQUOTE -> type(DQUOTE), popMode;

//mode INSIDE_CST_DOLLAR;
//CST_CONTENT : PROGNAME -> type(PROGNAME),pushMode(DEFAULT_MODE);
//CST_BLANK : BLANK -> type(BLANK);
//RPAREN : ')' -> popMode;

mode INSIDE_CST_BT;
CST_CONTENT_BT : PROGNAME -> type(PROGNAME);
CST_BLANK_BT : BLANK -> type(BLANK);
TAIL_BACKTICK : '`' -> popMode ;

