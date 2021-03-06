lexer grammar BashLexer;

VARNAME: [a-zA-Z_][a-zA-Z0-9_]*;
PUNCS: (~[a-zA-Z0-9= \t\n<>(){}'"|$&`;\\])+;
NUM: [0-9]+;
BLANK: [ \t]+;
EQ: '=';
VAR: '$' ( [$!@] | [a-zA-Z0-9_]+)?;
SQUOTE: '\'' -> pushMode(INSIDE_SQUOTE);
DQUOTE: '"' -> pushMode(INSIDE_DQUOTE);
LPAREN: '(' -> pushMode(DEFAULT_MODE);
DOLLAR_LPAREN: '$(' -> pushMode(DEFAULT_MODE);
LT_LPAREN: '<(' -> pushMode(DEFAULT_MODE);
GT_LPAREN: '>(' -> pushMode(DEFAULT_MODE);
BACKTICK: '`' -> pushMode(BT);
DOLLAR_DLPAREN: '$((' -> pushMode(ARITH);
DOLLAR_LCURLY: '${' -> pushMode(PARAM_EXPANSION);
ESC_CHAR: '\\' .;
LCURLY: '{';
RCURLY: '}';
SEMI: ';';
PIPE: '|';
PIPE_AND: '|&';
LT: '<';
GT: '>';
LT_AND: '<&';
GT_AND: '>&';
AND_GT: '&>';
AND_DGT: '&>>';
DLT: '<<';
TLT: '<<<';
DLT_DASH: '<<-';
DGT: '>>';
LTGT: '<>';
GTPIPE: '>|';
AND: '&';
NL: '\n' -> skip;
RPAREN : ')' -> popMode;

mode INSIDE_SQUOTE;
SQUOTE_VARNAME: VARNAME -> type(VARNAME);
SQUOTE_NUM: NUM -> type(NUM);
SQUOTE_CONTENT : (~['a-zA-Z0-9_] | '\\' .)+ -> type(PUNCS);
TAIL_SQUOTE: SQUOTE -> type(SQUOTE), popMode;

mode INSIDE_DQUOTE;
DQUOTE_VARNAME: VARNAME -> type(VARNAME);
DQUOTE_NUM: NUM -> type(NUM);
DQUOTE_CONTENT : (~["\\$<>`a-zA-Z0-9_] | '\\' .)+ -> type(PUNCS);
DQUOTE_VAR : VAR -> type(VAR);
DQUOTE_DOLLAR_LPAREN : DOLLAR_LPAREN -> type(DOLLAR_LPAREN), pushMode(DEFAULT_MODE);
DQUOTE_DOLLAR_DLPAREN: DOLLAR_DLPAREN -> pushMode(ARITH);
DQUOTE_LT : LT -> type(LT);
DQUOTE_GT : GT -> type(GT);
DQUOTE_LT_LPAREN : LT_LPAREN -> type(LT_LPAREN), pushMode(DEFAULT_MODE);
DQUOTE_GT_LPAREN : GT_LPAREN -> type(GT_LPAREN), pushMode(DEFAULT_MODE);
DQUOTE_DOLLAR_LCURLY: DOLLAR_LCURLY -> type(DOLLAR_LCURLY), pushMode(PARAM_EXPANSION);
DQUOTE_BACKTICK : BACKTICK -> type(BACKTICK), pushMode(BT);
TAIL_DQUOTE : DQUOTE -> type(DQUOTE), popMode;

mode ARITH;
ARITH_CONTENT : (~["$<>()`])+;
ARITH_VAR : VAR -> type(VAR);
ARITH_DQUOTE : DQUOTE -> type(DQUOTE), pushMode(INSIDE_DQUOTE);
ARITH_DOLLAR_LPAREN : DOLLAR_LPAREN -> type(DOLLAR_LPAREN), pushMode(DEFAULT_MODE);
ARITH_LT_LPAREN : LT_LPAREN -> type(LT_LPAREN), pushMode(DEFAULT_MODE);
ARITH_GT_LPAREN : GT_LPAREN -> type(GT_LPAREN), pushMode(DEFAULT_MODE);
ARITH_LPAREN : LPAREN -> type(LPAREN), pushMode(DEFAULT_MODE);
ARITH_BACKTICK : BACKTICK -> type(BACKTICK), pushMode(BT);
DRPAREN : '))' -> popMode;

mode PARAM_EXPANSION;
PARAM_VARNAME: VARNAME -> type(VARNAME);
PARAM_PUNCS: (~[-a-zA-Z0-9= \t\n<>(){}'"|$&`;:+?%#])+ -> type(PUNCS);
PARAM_NUM: NUM -> type(NUM);
PARAM_BLANK: BLANK -> type(BLANK);
PARAM_VAR: VAR -> type(VAR);
PARAM_SQUOTE: SQUOTE -> type(SQUOTE), pushMode(INSIDE_SQUOTE);
PARAM_DQUOTE: DQUOTE -> type(DQUOTE), pushMode(INSIDE_DQUOTE);
PARAM_LPAREN: LPAREN -> type(LPAREN), pushMode(DEFAULT_MODE);
PARAM_DOLLAR_LPAREN: DOLLAR_LPAREN -> type(DOLLAR_LPAREN), pushMode(DEFAULT_MODE);
PARAM_LT_LPAREN: LT_LPAREN -> type(LT_LPAREN), pushMode(DEFAULT_MODE);
PARAM_GT_LPAREN: GT_LPAREN -> type(GT_LPAREN), pushMode(DEFAULT_MODE);
PARAM_BACKTICK: BACKTICK -> type(BACKTICK), pushMode(BT);
PARAM_DOLLAR_DLPAREN: DOLLAR_DLPAREN -> type(DOLLAR_DLPAREN), pushMode(ARITH);
COMMA: ':';
DASH: '-';
PARAM_EQ: '=';
QMARK: '?';
PLUS: '+';
PERCENT: '%';
DPERCENT: '%%';
HASH: '#';
DHASH: '##';
PARAM_RCURLY: RCURLY -> type(RCURLY), popMode;

// almost a full copy, just for backtick
mode BT;
BT_VARNAME: VARNAME -> type(VARNAME);
BT_PUNCS: PUNCS -> type(PUNCS);
BT_NUM: NUM -> type(NUM);
BT_BLANK: BLANK -> type(BLANK);
BT_EQ: EQ -> type(EQ);
BT_VAR: VAR -> type(VAR);
BT_SQUOTE: SQUOTE -> type(SQUOTE),pushMode(INSIDE_SQUOTE);
BT_DQUOTE: DQUOTE -> type(DQUOTE), pushMode(INSIDE_DQUOTE);
BT_LPAREN: LPAREN -> type(LPAREN), pushMode(BT);
BT_DOLLAR_LPAREN: DOLLAR_LPAREN -> type(DOLLAR_LPAREN), pushMode(BT);
BT_LT_LPAREN: LT_LPAREN -> type(LT_LPAREN), pushMode(BT);
BT_GT_LPAREN: GT_LPAREN -> type(GT_LPAREN), pushMode(BT);
BT_BACKTICK: BACKTICK -> type(BACKTICK), popMode;
BT_DOLLAR_DLPAREN: DOLLAR_DLPAREN -> type(DOLLAR_DLPAREN), pushMode(ARITH);
BT_DOLLAR_LCURLY: DOLLAR_LCURLY -> type(DOLLAR_LCURLY), pushMode(PARAM_EXPANSION);
BT_ESC_CHAR: ESC_CHAR -> type(ESC_CHAR);
BT_LCURLY: LCURLY -> type(LCURLY);
BT_RCURLY: RCURLY -> type(RCURLY);
BT_SEMI: SEMI -> type(SEMI);
BT_PIPE: PIPE -> type(PIPE);
BT_PIPE_AND: PIPE_AND -> type(PIPE_AND);
BT_LT: LT -> type(LT);
BT_GT: GT -> type(GT);
BT_LT_AND: LT_AND -> type(LT_AND);
BT_GT_AND: GT_AND -> type(GT_AND);
BT_AND_GT: AND_GT -> type(AND_GT);
BT_AND_DGT: AND_DGT -> type(AND_DGT);
BT_DLT: DLT -> type(DLT);
BT_TLT: TLT -> type(TLT);
BT_DLT_DASH: DLT_DASH -> type(DLT_DASH);
BT_DGT: DGT -> type(DGT);
BT_LTGT: LTGT -> type(LTGT);
BT_GTPIPE: GTPIPE -> type(GTPIPE);
BT_AND: AND -> type(AND);
BT_NL: NL -> type(NL);
BT_RPAREN: RPAREN -> type(RPAREN);
