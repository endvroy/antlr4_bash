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
BACKTICK : '`' -> pushMode(INSIDE_BT);
DQUOTE : '"' -> pushMode(INSIDE_DQUOTE);
ARGS_BLANK : BLANK;
PIPE : '|' -> mode(DEFAULT_MODE);
ARGS_END: RPAREN -> popMode;

mode ASSIGN_RLS;
LITERAL: (~[$<>`()|'" \t])+;
RLS_SQUOTE_STR : SQUOTE_STR ;
RLS_VAR : '$' ( [$!] | [a-zA-Z0-9_]+)?;
RLS_DOLLAR_LPAREN : '$(' -> pushMode(DEFAULT_MODE);
RLS_BACKTICK : '`' -> pushMode(INSIDE_BT);
RLS_DQUOTE : '"' -> pushMode(INSIDE_DQUOTE);
RLS_BLANK: BLANK -> mode(DEFAULT_MODE);
RLS_END: RPAREN -> popMode;
// todo: add other cases

mode INSIDE_DQUOTE;
DQUOTE_CONTENT : (~["\\$] | '\\' [\\"])+;
DQUOTE_VAR : VAR -> type(VAR);
DQUOTE_DOLLAR_LPAREN : DOLLAR_LPAREN -> type(DOLLAR_LPAREN), pushMode(DEFAULT_MODE);
DQUOTE_BACKTICK : BACKTICK -> type(BACKTICK), pushMode(INSIDE_BT);
TAIL_DQUOTE : DQUOTE -> type(DQUOTE), popMode;

// almost a full copy, just for backtick
mode INSIDE_BT;
BT_PROGNAME : PROGNAME -> type(PROGNAME), mode(BT_NECK);
BT_BLANK : BLANK -> skip;
TAIL_BACKTICK : BACKTICK -> type(BACKTICK), popMode ;

mode BT_NECK;
BT_NECK_BLANK : BLANK -> skip, mode(BT_ARGS);
BT_EQ : EQ -> type(EQ), mode(BT_ASSIGN_RLS);

mode BT_ARGS;
BT_ARG: ARG -> type(ARG);
BT_SQUOTE_STR : SQUOTE_STR -> type(SQUOTE_STR);
BT_VAR : VAR -> type(VAR);
BT_DOLLAR_LPAREN : DOLLAR_LPAREN -> type(DOLLAR_LPAREN), pushMode(INSIDE_BT);
BT_DQUOTE : DQUOTE -> type(DQUOTE), pushMode(INSIDE_DQUOTE);
BT_ARGS_BLANK : BLANK -> type(ARGS_BLANK);
BT_PIPE : PIPE -> type(PIPE), mode(INSIDE_BT);
BT_BACKTICK : BACKTICK -> type(BACKTICK), popMode;

mode BT_ASSIGN_RLS;
BT_LITERAL: LITERAL -> type(LITERAL);
BT_RLS_SQUOTE_STR : SQUOTE_STR -> type(SQUOTE_STR) ;
BT_RLS_VAR : RLS_VAR -> type(RLS_VAR);
BT_RLS_DOLLAR_LPAREN : DOLLAR_LPAREN -> type(DOLLAR_LPAREN), pushMode(INSIDE_BT);
BT_RLS_DQUOTE : DQUOTE -> type(DQUOTE), pushMode(INSIDE_DQUOTE);
BT_RLS_BLANK: BLANK -> type(RLS_BLANK), mode(INSIDE_BT);
BT_RLS_BACKTICK : BACKTICK -> type(BACKTICK), popMode;

