parser grammar BashParser;

options {tokenVocab=BashLexer;}

pipeline : pipeline PIPE cmd
| cmd;

cmd : ((assign_list BLANK)? exec | assign_list) BLANK?;

assign_list : assign_list BLANK assign
| assign;

assign: NAME EQ assign_rls;

assign_rls : (LITERAL | SQUOTE_STR | VAR | dquote_str | subst)*;

exec: prog redir? (BLANK cmd_suffix)?;

prog : (NAME | NUM | VAR | SQUOTE_STR | dquote_str | subst)+;

redir : NUM redir_op arg
| redir_op arg;

redir_op : LT
| GT
| LT_AND
| GT_AND
| AND_GT
| AND_DGT
| DLT
| TLT
| DLT_DASH
| DGT
| LTGT
| GTPIPE;

cmd_suffix : cmd_suffix BLANK (redir | arg)
| (redir | arg);

arg: (NAME | NUM | SQUOTE_STR | VAR | dquote_str | subst)+;

dquote_str : DQUOTE (DQUOTE_CONTENT | VAR | subst)* DQUOTE;

subst : cst | lpst | rpst;

cst : DOLLAR_LPAREN pipeline? RPAREN
| BACKTICK pipeline? BACKTICK
;

lpst : LT_LPAREN pipeline? RPAREN;

rpst : GT_LPAREN pipeline? RPAREN;
