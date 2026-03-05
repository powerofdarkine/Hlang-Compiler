from utils import Tokenizer


def test_001():
    """Test empty input"""
    source = ""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_002():
    """Test keywords recognition"""
    source = "func main if else while for let const"
    expected = "func,main,if,else,while,for,let,const,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_003():
    """Test integer literals"""
    source = "42 0 -17 007"
    expected = "42,0,-,17,007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_004():
    """Test float literals"""
    source = "3.14 -2.5 0.0 42. .5"
    expected = "3.14,-,2.5,0.0,42.,.,5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
def test_005():
    """Test identifiers"""
    source = "x y_var myFunc123"
    expected = "x,y_var,myFunc123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    """Test operators"""
    source = "+ - * / == != <= >= ="
    expected = "+,-,*,/,==,!=,<=,>=,=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
    """Test delimiters"""
    source = "( ) { } [ ] ; , ."
    expected = "(,),{,},[,],;,,,.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    """Test string literals"""
    source = '"hello" "world" ""'
    expected = 'hello,world,,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    """Test mixed types"""
    source = "let x = 42 + 3.14;"
    expected = "let,x,=,42,+,3.14,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_010():
    """Test comments (if tokenizer skips them)"""
    source = "x = 5 // this is a comment"
    expected = "x,=,5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_011():
    """Test newline handling"""
    source = "x = 1\ny = 2"
    expected = "x,=,1,y,=,2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_012():
    """Test scientific float notation"""
    source = "1e3 2.5e-4"
    expected = "1,e3,2.5e-4,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_013():
    """Test unary minus with float"""
    source = "-3.14"
    expected = "-,3.14,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    """Test escape sequences in strings"""
    source = '"line\\nbreak"'
    expected = 'line\\nbreak,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    """Test plus operator with whitespace"""
    source = "a + b"
    expected = "a,+,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    """Test minus operator with no whitespace"""
    source = "a-b"
    expected = "a,-,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    """Test multiplication and division"""
    source = "x*y/z"
    expected = "x,*,y,/,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    """Test assignment and equality operators"""
    source = "x = 5 == y"
    expected = "x,=,5,==,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    """Test parentheses and brackets"""
    source = "(a[0])"
    expected = "(,a,[,0,],),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    """Test curly braces and semicolon"""
    source = "{ let x = 10; }"
    expected = "{,let,x,=,10,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    """Test comma separated values"""
    source = "1, 2, 3"
    expected = "1,,,2,,,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    """Test function declaration"""
    source = "func add(a, b) { return a + b; }"
    expected = "func,add,(,a,,,b,),{,return,a,+,b,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    """Test if-else block"""
    source = "if (x > 0) { y = 1; } else { y = -1; }"
    expected = "if,(,x,>,0,),{,y,=,1,;,},else,{,y,=,-,1,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    """Test while loop"""
    source = "while (i < 10) { i = i + 1; }"
    expected = "while,(,i,<,10,),{,i,=,i,+,1,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    """Test for loop"""
    source = "for (let i = 0; i < 10; i = i + 1) {}"
    expected = "for,(,let,i,=,0,;,i,<,10,;,i,=,i,+,1,),{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    """Test nested expressions"""
    source = "(a + (b * c))"
    expected = "(,a,+,(,b,*,c,),),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    """Test boolean literals"""
    source = "true false"
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    """Test null literal"""
    source = "null"
    expected = "null,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    """Test chained comparisons"""
    source = "x < y && y < z"
    expected = "x,<,y,&&,y,<,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    """Test logical OR operator"""
    source = "a || b"
    expected = "a,||,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    """Test increment operator"""
    source = "i+i"
    expected = "i,+,i,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    """Test decrement operator"""
    source = "j-j"
    expected = "j,-,j,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    """Test compound assignment"""
    source = "x += 10"
    expected = "x,+,=,10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
    """Test ternary operator"""
    source = "x * y : z"
    expected = "x,*,y,:,z,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    """Test multi-line string (if supported)"""
    source = '"line1\\nline2"'
    expected = 'line1\\nline2,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    """Test hexadecimal number"""
    source = "0 x1A3F"
    expected = "0,x1A3F,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    """Test binary number"""
    source = "b1011"
    expected = "b1011,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    """Test octal number"""
    source = "75x"
    expected = "75,x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    """Test unterminated string literal"""
    source = '"unterminated'
    expected = "Unclosed String: unterminated"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    """Test unknown character"""
    source = "@"
    expected = "Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_041():
    """Test multiple lines"""
    source = "x = 1\ny = 2\nz = 3"
    expected = "x,=,1,y,=,2,z,=,3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_042():
    """Test tab characters"""
    source = "a\tb"
    expected = "a,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_043():
    """Test string with escaped quote"""
    source = '"He said, \"hi\""'
    expected = 'He said, ,hi,,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_044():
    """Test complex expression"""
    source = "(a + b) * (c - d) / e"
    expected = "(,a,+,b,),*,(,c,-,d,),/,e,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_045():
    """Test float with exponent"""
    source = "1.5e10"
    expected = "1.5e10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_046():
    """Test negative float with exponent"""
    source = "-2.3e-4"
    expected = "-,2.3e-4,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_047():
    """Test identifier with underscores"""
    source = "_my_var"
    expected = "_my_var,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_048():
    """Test keyword with surrounding identifiers"""
    source = "mainly main"
    expected = "mainly,main,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_049():
    """Test long numeric literal"""
    source = "1234567890"
    expected = "1234567890,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_050():
    """Test empty string literal"""
    source = '""'
    expected = ",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_051():
    """Test escaped backslash in string"""
    source = "\"C:\\\\path\""
    expected = "C:\\\\path,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_052():
    """Test string with unicode character"""
    source = '"*#?"'
    expected = '*#?,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_053():
    """Test identifier starting with underscore"""
    source = "_temp"
    expected = "_temp,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_054():
    """Test multiple operators together"""
    source = "x+=y-=z*=w/=q"
    expected = "x,+,=,y,-,=,z,*,=,w,/,=,q,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    """Test float with leading dot"""
    source = ".75"
    expected = ".,75,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_056():
    """Test float with trailing dot"""
    source = "8."
    expected = "8.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_057():
    """Test large hexadecimal value"""
    source = "FFFFFFFF"
    expected = "FFFFFFFF,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_058():
    """Test line comment skipping"""
    source = "let x = 5; // comment here"
    expected = "let,x,=,5,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_059():
    """Test multiline comment skipping"""
    source = "/* comment \n over lines */ let x = 1;"
    expected = "let,x,=,1,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_060():
    """Test nested comments (if not supported)"""
    source = "/* outer /* inner */ still */ x"
    expected = "x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_061():
    """Test escaped characters in string"""
    source = '"hello" "world"'
    expected = 'hello,world,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    """Test escape tab in string"""
    source = '"hello world"'
    expected = 'hello world,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    """Test combination of literals and operators"""
    source = "42 + 3.14 - x"
    expected = "42,+,3.14,-,x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    """Test chained assignments"""
    source = "a = b = c = 1"
    expected = "a,=,b,=,c,=,1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_065():
    """Test long identifier name"""
    source = "this_is_a_very_long_identifier_name"
    expected = "this_is_a_very_long_identifier_name,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_066():
    """Test mixed identifiers and numbers"""
    source = "x1 y2 z3"
    expected = "x1,y2,z3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_067():
    """Test exponent float with plus sign"""
    source = "2.5e+8"
    expected = "2.5e+8,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    """Test identifier with digits in middle"""
    source = "var123name"
    expected = "var123name,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    """Test unterminated comment (should error or EOF)"""
    source = "/* unfinished comment*/"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_070():
    """Test dollar sign in identifier (if supported)"""
    source = "$value"
    expected = "Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_071():
    """Test percent sign usage"""
    source = "x % 2"
    expected = "x,%,2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_072():
    """Test bitwise operators"""
    source = "x & y | z ^ w"
    expected = "x,Error Token &"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    """Test shift operators"""
    source = "x 2 >> 1"
    expected = "x,2,>>,1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    """Test null coalescing operator (if supported)"""
    source = "x ? y"
    expected = "x,Error Token ?"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    """Test optional chaining operator (if supported)"""
    source = "a?.b"
    expected = "a,Error Token ?"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    """Test boolean expression with parentheses"""
    source = "(true && false)"
    expected = "(,true,&&,false,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    """Test floating point with no integer part"""
    source = ".123"
    expected = ".,123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_078():
    """Test floating point with no fractional part"""
    source = "123."
    expected = "123.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    """Test function call with multiple arguments"""
    source = "sum(1, 2, 3)"
    expected = "sum,(,1,,,2,,,3,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    """Test arrow function syntax (if supported)"""
    source = "x = x + 1"
    expected = "x,=,x,+,1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_081():
    """Test nested function calls"""
    source = "print(sum(1,2))"
    expected = "print,(,sum,(,1,,,2,),),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    """Test multiple string literals with spaces"""
    source = '"a" "b" "c"'
    expected = 'a,b,c,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    """Test exponential notation float"""
    source = "6.022e23"
    expected = "6.022e23,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_084():
    """Test invalid character at start"""
    source = "#abc"
    expected = "Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    """Test identifier with mixed case"""
    source = "CamelCase123"
    expected = "CamelCase123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    """Test float with exponent only"""
    source = "1.0e9"
    expected = "1.0e9,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_087():
    """Test simple math expression with variables"""
    source = "a + b * c - d / e"
    expected = "a,+,b,*,c,-,d,/,e,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_088():
    """Test deeply nested expressions"""
    source = "(((((x)))))"
    expected = "(,(,(,(,(,x,),),),),),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_089():
    """Test ternary nested expressions"""
    source = "x + y : z = a : b"
    expected = "x,+,y,:,z,=,a,:,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_090():
    """Test comment only line"""
    source = "// just a comment"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_091():
    """Test empty string with whitespace before/after"""
    source = '  ""  '
    expected = ',EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_092():
    """Test operators as part of string"""
    source = '"a+b=c"'
    expected = 'a+b=c,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_093():
    """Test function call with no arguments"""
    source = "doSomething()"
    expected = "doSomething,(,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_094():
    """Test deeply nested brackets and braces"""
    source = "[{(([]))}]"
    expected = "[,{,(,(,[,],),),},],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_095():
    """Test backtick character (if unsupported)"""
    source = "`template`"
    expected = "Error Token `"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_096():
    """Test multiple equal signs"""
    source = "x == y"
    expected = "x,==,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    """Test identifier starting with digit (invalid)"""
    source = "1abc"
    expected = "1,abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_098():
    """Test spread operator (if supported)"""
    source = "...args"
    expected = ".,.,.,args,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    """Test line break in string (if allowed)"""
    source = '"\\n"'
    expected = '\\n,EOF'
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_100():
    """Test underscore as a number separator (if supported)"""
    source = "_000_000"
    expected = "_000_000,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected




