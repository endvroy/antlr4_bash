parser grammar BashParser;

options {tokenVocab=BashLexer;}

pipeline : pipeline PIPE cmd
| cmd;

cmd : BLANK? ((exec_prefix BLANK)? exec | exec_prefix) BLANK?;

exec_prefix : exec_prefix (BLANK? redir | BLANK assign)
| (redir | assign);

assign: VARNAME EQ assign_rls;

assign_rls : (VARNAME | PUNCS | NUM | squote_str | VAR | dquote_str | subst)*;

exec: prog exec_suffix?;

prog : VARNAME (VARNAME | PUNCS | NUM | VAR | squote_str | dquote_str | subst)*
| (PUNCS | NUM | EQ | VAR | squote_str | dquote_str | subst)
(VARNAME | PUNCS | NUM | EQ | VAR | squote_str | dquote_str | subst)*;

exec_suffix : exec_suffix (BLANK? redir | BLANK arg)
| (BLANK? redir | BLANK arg);

redir : NUM redir_op BLANK? arg
| redir_op BLANK? arg;

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

arg: (VARNAME | PUNCS | ESC_CHAR | AND | EQ | NUM | squote_str | VAR | dquote_str | subst | pure_curly)+;

dquote_str : DQUOTE (VARNAME | NUM | PUNCS | LT | GT | VAR | subst)* DQUOTE;

squote_str : SQUOTE (VARNAME | PUNCS | NUM)* SQUOTE;

subst : cst | lpst | rpst | arith | param_exp;

cst : DOLLAR_LPAREN pipeline? RPAREN
| BACKTICK pipeline? BACKTICK
;

lpst : LT_LPAREN pipeline? RPAREN;

rpst : GT_LPAREN pipeline? RPAREN;

arith : DOLLAR_DLPAREN (VARNAME | NUM | VAR | PUNCS | subst)* DRPAREN; //todo: fill in proper body for arith

param_exp: DOLLAR_LCURLY (VARNAME | NUM | VAR | PUNCS | subst)+ RCURLY;

grp : paren_grp | curly_grp;

paren_grp : LPAREN pipeline RPAREN;

pure_curly: LCURLY | RCURLY;

curly_grp : LCURLY pipeline SEMI BLANK? RCURLY;  // todo: check for leading blank after LCURLY in actions
