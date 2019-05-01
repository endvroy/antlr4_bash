parser grammar BashParser;

options {tokenVocab=BashLexer;}

pipeline : pipeline PIPE cmd
| cmd;

cmd : BLANK? ((exec_prefix BLANK)? exec | exec_prefix) BLANK?;

exec_prefix : exec_prefix BLANK (redir | assign)
| (redir | assign);

assign: VARNAME EQ assign_rls;

assign_rls : (VARNAME | NAME | NUM | SQUOTE_STR | VAR | dquote_str | subst | redir)*;

exec: prog redir? (BLANK exec_suffix)?;

prog : VARNAME (VARNAME | NAME | NUM | VAR | SQUOTE_STR | dquote_str | subst)*
| (NAME | NUM | EQ | VAR | SQUOTE_STR | dquote_str | subst)
(VARNAME | NAME | NUM | EQ | VAR | SQUOTE_STR | dquote_str | subst)*;

exec_suffix : exec_suffix BLANK (redir | arg)
| (redir | arg);

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

arg: (VARNAME | NAME | ESC_CHAR | EQ | NUM | SQUOTE_STR | VAR | dquote_str | subst | pure_curly)+;

dquote_str : DQUOTE (DQUOTE_CONTENT | LT | GT | VAR | subst)* DQUOTE;

subst : cst | lpst | rpst | arith | param_exp;

cst : DOLLAR_LPAREN pipeline? RPAREN
| BACKTICK pipeline? BACKTICK
;

lpst : LT_LPAREN pipeline? RPAREN;

rpst : GT_LPAREN pipeline? RPAREN;

arith : DOLLAR_DLPAREN pipeline? DRPAREN; //todo: fill in proper body for arith

param_exp: DOLLAR_LCURLY VARNAME (param_exp_op BLANK? assign_rls)? RCURLY
| DOLLAR_LCURLY POUND VARNAME RCURLY;

param_exp_op: COMMA (DASH | EQ | QMARK | PLUS)
| PERCENT | DPERCENT | POUND | DPOUND;

grp : paren_grp | curly_grp;

paren_grp : LPAREN pipeline RPAREN;

pure_curly: LCURLY | RCURLY;

curly_grp : LCURLY pipeline SEMI BLANK? RCURLY;  // todo: check for leading blank after LCURLY in actions
