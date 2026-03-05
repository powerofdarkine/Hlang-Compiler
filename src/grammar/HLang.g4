grammar HLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.STRINGLIT:
        result = super().emit();
        result.text = result.text[1:-1]
        return result
    elif tk == self.UNCLOSE_STRING:       
        result = super().emit();
        result.text = result.text[1:];
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        text = result.text[1:-1]
        for i in range(len(text) - 1):
            if text[i] == '\\' and text[i+1]==' ' and i+1!=len(text)-1:
                continue;
            elif text[i] == '\\' and text[i+1] not in 'tnr"\\':
                # found an illegal escape: e.g. "\q"
                bad_seq = text[:i+2]
                raise IllegalEscape(bad_seq)
            


        raise IllegalEscape(text)

    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// Keywords
BOOL     : 'bool';
BREAK    : 'break';
CONST    : 'const';
CONTINUE : 'continue';
ELSE     : 'else';
FALSE    : 'false';
//AA: '++';
//MM:'--';

FLOAT    : 'float';
FOR      : 'for';
FUNC     : 'func';
IF       : 'if';
IN       : 'in';
INT      : 'int';

LET      : 'let';
RETURN   : 'return';
STRING   : 'string';
TRUE     : 'true';
VOID     : 'void';
WHILE    : 'while';
// Arithmetic Operators
ADD        : '+';
SUB        : '-';
MUL        : '*';
DIV        : '/';
MOD        : '%';

// Comparison Operators
EQ         : '==';
NEQ        : '!=';
LT         : '<';
LE         : '<=';
GT         : '>';
GE         : '>=';
// Logical Operators
AND        : '&&';
OR         : '||';
NOT        : '!';
// Assignment Operator
ASSIGN     : '=';
// Type Annotation
COLON      : ':';
// Function Return Type
RET_TYPE   : '->';
// Pipeline Operator
PIPE       : '>>';
// Brackets and Delimiters
LPAREN     : '(';
RPAREN     : ')';
LBRACK     : '[';
RBRACK     : ']';
LBRACE     : '{';
RBRACE     : '}';
COMMA      : ',';
SEMI       : ';';
DOT        : '.';
DQ: '"';

fragment DIGIT: [0-9]+;
fragment CHAR: ~["\\\u0000-\u001F\u007F-\uFFFF];
fragment ESCSEQ: '\\' [tnr"\\];
INTLIT:  DIGIT;
FLOATLIT: DIGIT DOT ((DIGIT)? ([Ee][+-]? DIGIT)?)?;
STRINGLIT: '"' (CHAR | ESCSEQ)* '"';
ID: [a-zA-Z_][a-zA-Z0-9_]*;
LINE_COMMENT: '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT: '/*' .* '*/' -> skip ;



program: dec res EOF;
array: LBRACK (ele elelist)? RBRACK;
ele: INTLIT|FLOATLIT|TRUE|FALSE|STRINGLIT|array;
elelist: COMMA ele elelist|;
res: funcd res|;
exp: exp PIPE exp0 | exp0;
exp0: exp0 OR exp1 | exp1;
exp1: exp1 AND exp2 | exp2;
exp2: exp2 EQ exp3 | exp2 NEQ exp3 | exp3;
exp3: exp3 LT exp4 | exp3 LE exp4 | exp3 GT exp4 | exp3 GE exp4 | exp4;
exp4: exp4 ADD exp5 | exp4 SUB exp5 | exp5;
exp5: exp5 MUL exp6 | exp5 DIV exp6 | exp5 MOD exp6 | exp6;
exp6: NOT exp6 | SUB exp6 | ADD exp6 | exp7;
exp7 : ele|callable;
callable: ID  fu arracc  |INT fu arracc|FLOAT fu arracc|array fu arracc |LPAREN exp RPAREN fu arracc|INTLIT fu arracc|STRINGLIT fu arracc|FLOATLIT fu arracc ;
//postfix: LPAREN (exp cm)? RPAREN postfix | LBRACK exp RBRACK postfix|;
fu:LPAREN (exp cm)? RPAREN fu| ;
arracc: LBRACK exp RBRACK arracc|;
cm:COMMA exp cm|;
dec: const* funcd*| ;
const: 'const' ID opt? ASSIGN exp SEMI;
opt:(COLON mtype)|(COLON arr);
arr: LBRACK arrs RBRACK;
arrs: LBRACK arrs RBRACK SEMI INTLIT|  mtype SEMI INTLIT;
mtype: INT|FLOAT|BOOL|STRING;
funcd: FUNC ID LPAREN para RPAREN RET_TYPE (mtype|VOID|arr) body;
para: ID COLON (mtype|arr) paralst|;
paralst: ',' ID COLON (mtype|arr) paralst|;
body: LBRACE inside RBRACE;
inside:stat inside| ;
stat: var SEMI| assign SEMI| condition| loop|body| smallstate SEMI| exp SEMI;
var: LET ID opt? ASSIGN exp;
assign: ID asspara ASSIGN exp;
asspara: LBRACK exp RBRACK asspara|;
condition: IF LPAREN exp RPAREN body cond (ELSE body)?;
cond: ELSE IF LPAREN exp RPAREN body cond | ;
loop: (WHILE LPAREN exp RPAREN body)|(FOR LPAREN ID 'in' exp RPAREN body);
smallstate: BREAK|CONTINUE| RETURN exp?;




//arraylst: ele elelist|;
//re: dec res;
//post: exp cm|;
//literal: INTLIT| FLOATLIT| TRUE| FALSE| STRINGLIT| array|LPAREN exp RPAREN ;
//ulti: mtype SEMI INTLIT;
//break: BREAK;
//continue: CONTINUE;
//return: RETURN (exp|);
//block: body;
//asspara: LBRACK (exp|) RBRACK asspara|;
//pa: exp|;
//for: FOR LPAREN ID 'in' exp RPAREN body;





















WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs 

ERROR_CHAR: . { raise ErrorToken(self.text); };
ILLEGAL_ESCAPE: '"' (CHAR|ESCSEQ)* '\\' (~[tnr"\\]) .*?  '"';
UNCLOSE_STRING
    : '"' (CHAR | ESCSEQ)* ( '\r'? '\n' | EOF ) 
    ;
