lexer grammar BashLexer;

SQUOTE_STR : '\'' (~['\\] | '\\' [\\'])* '\'' ;
PROGNAME : ('a'..'z'|'A'..'Z'|'0'..'9')+ ;
BLANK : [ \t]+ ;
