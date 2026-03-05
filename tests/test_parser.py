from utils import Parser

def test_001():
    """Test empty function declaration"""
    source = """func main() -> void { }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    """Test function with parameters"""
    source = """func add(a: int, b: int) -> int { return a + b; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_003():
    """Test variable declaration with type annotation"""
    source = """func main() -> void { let x: int = 42; }"""
    expected = "success"
    assert Parser(source).parse() == expected 
    
def test_004():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name => \"Alice\"; }"""
    expected = "Error on line 1 col 32: >"
    assert Parser(source).parse() == expected

def test_005():
    """Test return statement"""
    source = """func main() -> int { return 1; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_006():
    """Test arithmetic expression"""
    source = """func calc() -> int { return 1 + 2 * 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_007():
    """Test invalid variable declaration (missing equals)"""
    source = """func main() -> void { let x 1; }"""
    expected = "Error on line 1 col 28: 1"
    assert Parser(source).parse() == expected

def test_008():
    """Test if-else statement"""
    source = """func main() -> void { if (x > 0) { x = x - 1; } else { x = x + 1; } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_009():
    """Test missing function body"""
    source = """func main() -> void"""
    expected = "Error on line 1 col 19: <EOF>"
    assert Parser(source).parse() == expected

def test_010():
    """Test nested blocks"""
    source = """const a = 1; 
    func main() -> void { { let x = 1; { let y = 2; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_011():
    """Test function call"""
    source = """func main() -> void { print(123); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_012():
    """Test boolean literals"""
    source = """func check() -> void { let x = true let y = false }"""
    expected = "Error on line 1 col 36: let"
    assert Parser(source).parse() == expected

def test_013():
    """Test unclosed block"""
    source = """func main() -> void { let x = 1; """
    expected = "Error on line 1 col 33: <EOF>"
    assert Parser(source).parse() == expected

def test_014():
    """Test unary minus operator"""
    source = """func main() -> int { return -5; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_015():
    """Test comparison operators"""
    source = """func main() -> bool { return 3 > 2 && 2 < 4; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_016():
    """Test equality operators"""
    source = """func main() -> bool { return 1 == 1 || 1 != 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_017():
    """Test missing semicolon"""
    source = """func main() -> void { let x = 5 let y = 6; }"""
    expected = "Error on line 1 col 32: let"
    assert Parser(source).parse() == expected

def test_018():
    """Test nested function call in return"""
    source = """const abc = foo();
    func main() -> int { return add(1, add(2, 3)); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_019():
    """Test multiple variable declarations"""
    source = """const foo = array[1][2][a1[2]];
    func main() -> void { let x = 1; let y = 2; let z = x + y; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_020():
    """Test if statement missing parentheses"""
    source = """func main() -> void { if x > 0 { return; } }"""
    expected = "Error on line 1 col 25: x"
    assert Parser(source).parse() == expected

def test_021():
    """Test assignment statement"""
    source = """func main() -> void { let x = 0; x = 10; y = x;}"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_022():
    """Test empty block inside if"""
    source = """func main() -> void { if (true) { } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_023():
    """Test comment in code (assuming tokenizer ignores)"""
    source = """func main() -> void { let x = 1; 
    // comment 
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_024():
    """Test invalid parameter declaration"""
    source = """func add(a int, b int) -> int { return a + b; }"""
    expected = "Error on line 1 col 11: int"
    assert Parser(source).parse() == expected

def test_025():
    """Test valid multiple returns (unreachable allowed)"""
    source = """func main() -> int { return 1; return 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_026():
    """Test function with multiple returns"""
    source = """func calc() -> int { let x = 2; return x * 2; return x + 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_027():
    """Test function with missing semicolon"""
    source = """func main() -> void { let x = 1 let y = 2; }"""
    expected = "Error on line 1 col 32: let"
    assert Parser(source).parse() == expected

def test_028():
    """Test nested if with else"""
    source = """func main() -> void { if (true) { if (false) { } else { } } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_029():
    """Test invalid function declaration (missing parens)"""
    source = """func invalid -> void { }"""
    expected = "Error on line 1 col 13: ->"
    assert Parser(source).parse() == expected

def test_030():
    """Test valid complex function with declarations and return"""
    source = """func compute() -> int { let a = 2; let b = 3; let c = a * b; return c; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_031():
    """Test while with no body"""
    source = """func loop() -> void { while (false); }"""
    expected = "Error on line 1 col 35: ;"
    assert Parser(source).parse() == expected

def test_032():
    """Test nested blocks with return"""
    source = """func main() -> int { { { let x = 1; return x; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_033():
    """Test if with no condition"""
    source = """func broken() -> void { if { let x = 1; } }"""
    expected = "Error on line 1 col 27: {"
    assert Parser(source).parse() == expected

def test_034():
    """Test valid for loop with nested scope"""
    source = """func main() -> void { for (i = 0; i < 5; i = i + 1) { { let y = i; } } }"""
    expected = "Error on line 1 col 29: ="
    assert Parser(source).parse() == expected

def test_035():
    """Test invalid return outside function"""
    source = """return 1;"""
    expected = "Error on line 1 col 0: return"
    assert Parser(source).parse() == expected

def test_036():
    """Test function with parameter and nested if"""
    source = """func logic(x: int) -> int { if (x > 0) { return x; } else { return -x; } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_037():
    """Test declaration followed by reassignment"""
    source = """func run() -> void { let z = 3; z = z + 1; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_038():
    """Test multiple types and return statement"""
    source = """func mix() -> int { let a: int = 2; let b = 3; return a + b; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_039():
    """Test missing function keyword"""
    source = """main() -> void { let x = 1; }"""
    expected = "Error on line 1 col 0: main"
    assert Parser(source).parse() == expected

def test_040():
    """Test empty return statement"""
    source = """func main() -> void { return; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_041():
    """Test extra closing brace"""
    source = """func test() -> void { let x = 1; }}"""
    expected = "Error on line 1 col 34: }"
    assert Parser(source).parse() == expected

def test_042():
    """Test function with no body"""
    source = """func ghost() -> void"""
    expected = "Error on line 1 col 20: <EOF>"
    assert Parser(source).parse() == expected

def test_043():
    """Test long statement sequence"""
    source = """func sequence() -> void { let a = 1; let b = 2; let c = 3; let d = 4; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_044():
    """Test chained addition and assignment"""
    source = """func math() -> void { let x = 1 + 2 + 3; x = x + 4; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_045():
    """Test nested loops and returns"""
    source = """func nested() -> int { while (true) { for (let i = 0; i < 1; i = i + 1) { return i; } } }"""
    expected = "Error on line 1 col 43: let"
    assert Parser(source).parse() == expected

def test_046():
    """Test broken variable declaration"""
    source = """func main() -> void { let = 1; }"""
    expected = "Error on line 1 col 26: ="
    assert Parser(source).parse() == expected

def test_047():
    """Test valid return in nested block"""
    source = """func work() -> int { { let x = 5; return x; } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_048():
    """Test double function declaration in same block"""
    source = """func one() -> void { } func two() -> void { }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_049():
    """Test unclosed string literal (should be error if tokenizer doesn't fix it)"""
    source = """func main() -> void { let s = \"unclosed; }"""
    expected = "Unclosed String: unclosed; }"
    assert Parser(source).parse() == expected

def test_050():
    """Test return with math expression"""
    source = """func calc() -> int { return (2 + 3) * 4; }"""
    expected = "success"
    assert Parser(source).parse() == expected

...

def test_051():
    """Test multiple returns with nested if"""
    source = """func check() -> int { if (true) { return 1; } return 0; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_052():
    """Test missing arrow in function declaration"""
    source = """func fail() void { let x = 1; }"""
    expected = "Error on line 1 col 12: void"
    assert Parser(source).parse() == expected

def test_053():
    """Test string with escape character"""
    source = """func main() -> void { let s = \"line1\\nline2\"; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_054():
    """Test return with float"""
    source = """func pi() -> float { return 3.14; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_055():
    """Test wrong assignment without value"""
    source = """func main() -> void { let x = ; }"""
    expected = "Error on line 1 col 30: ;"
    assert Parser(source).parse() == expected

def test_056():
    """Test correct use of logical operators"""
    source = """func logic() -> bool { return true && false || true; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_057():
    """Test function with no return in non-void function"""
    source = """func bad() -> int { let x = 1; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_058():
    """Test deep nesting of blocks"""
    source = """func deep() -> void { { { { { let x = 1; } } } } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_059():
    """Test invalid identifier name (starting with number)"""
    source = """func main() -> void { let 1abc = 5; }"""
    expected = "Error on line 1 col 26: 1"
    assert Parser(source).parse() == expected

def test_060():
    """Test if-else inside while"""
    source = """func main() -> void { while (true) { if (false) { break; } else { continue; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_061():
    """Test call with too many commas"""
    source = """func main() -> void { print(1,,2); }"""
    expected = "Error on line 1 col 30: ,"
    assert Parser(source).parse() == expected

def test_062():
    """Test arithmetic with parentheses"""
    source = """func calc() -> int { return (1 + 2) * (3 + 4); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_063():
    """Test function with only comment"""
    source = """func comment() -> void { // just a comment }"""
    expected = "Error on line 1 col 44: <EOF>"
    assert Parser(source).parse() == expected

def test_064():
    """Test invalid return type"""
    source = """func error() -> unknown { return 0; }"""
    expected = "Error on line 1 col 16: unknown"
    assert Parser(source).parse() == expected

def test_065():
    """Test complex boolean expression"""
    source = """func logic() -> bool { return !(false || true) && (true && true); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_066():
    """Test mismatched brackets"""
    source = """func main() -> void { let arr = [1, 2, 3; }"""
    expected = "Error on line 1 col 40: ;"
    assert Parser(source).parse() == expected

def test_067():
    """Test valid variable shadowing"""
    source = """func shadow() -> void { let x = 1; { let x = 2; } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_068():
    """Test empty parameter list spacing"""
    source = """func empty ( ) -> void { }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_069():
    """Test invalid multiple type keywords"""
    source = """func fail() -> int void { return 1; }"""
    expected = "Error on line 1 col 19: void"
    assert Parser(source).parse() == expected

def test_070():
    """Test valid nested if else with return"""
    source = """func branch(x: int) -> int { if (x > 0) { return 1; } else if (x == 0) { return 0; } else { return -1; } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_071():
    """Test stray closing parenthesis"""
    source = """func main() -> void { let x = 1); }"""
    expected = "Error on line 1 col 31: )"
    assert Parser(source).parse() == expected

def test_072():
    """Test string literal with semicolon inside"""
    source = """func main() -> void { let s = \"abc;def\"; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_073():
    """Test assignment to literal (invalid)"""
    source = """func main() -> void { 5 = x; }"""
    expected = "Error on line 1 col 24: ="
    assert Parser(source).parse() == expected

def test_074():
    """Test void function with no return"""
    source = """func noop() -> void { let done = true; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_075():
    """Test valid multiple nested scopes"""
    source = """func layers() -> void { { { let x = 0; } { let y = 1; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected



def test_076():
    """Test valid if-else with variable declaration"""
    source = """func cond() -> void { if (true) { let x = 1; } else { let x = 2; } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_077():
    """Test missing closing brace in function"""
    source = """func broken() -> void { let x = 1; """
    expected = "Error on line 1 col 35: <EOF>"
    assert Parser(source).parse() == expected

def test_078():
    """Test valid arithmetic with nested expressions"""
    source = """func math() -> int { return ((1 + 2) * 3) - 4; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_079():
    """Test assignment without variable keyword"""
    source = """func main() -> void { x = 5; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_080():
    """Test multiple return types in signature"""
    source = """func conflict() -> int -> void { return 1; }"""
    expected = "Error on line 1 col 23: ->"
    assert Parser(source).parse() == expected

def test_081():
    """Test nested while loops"""
    source = """func loop() -> void { while (true) { while (false) { break; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_082():
    """Test variable name with underscore"""
    source = """func main() -> void { let _val = 100; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_083():
    """Test assignment with undeclared variable"""
    source = """func main() -> void { y = 10; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_084():
    """Test break outside loop"""
    source = """func main() -> void { break; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_085():
    """Test continue outside loop"""
    source = """func main() -> void { continue; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_086():
    """Test return void with value (should fail if strict)"""
    source = """func main() -> void { return 1; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_087():
    """Test return with no value in int function"""
    source = """func num() -> int { return; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_088():
    """Test multiple variable declaration in one line (if allowed)"""
    source = """func main() -> void { let x = 1; let y = 2; let z = 3; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_089():
    """Test valid expression with all operators"""
    source = """func calc() -> int { return 1 + 2 - 3 * 4 / 5; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_090():
    """Test too many parameters in function declaration"""
    source = """func crazy(a: int, b: int, c: int, d: int, e: int, f: int) -> void { }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_091():
    """Test invalid return type format"""
    source = """func wrong() -> int float { return 5; }"""
    expected = "Error on line 1 col 20: float"
    assert Parser(source).parse() == expected

def test_092():
    """Test call with no arguments"""
    source = """func call() -> void { print(); }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_093():
    """Test if condition with assignment (should be invalid)"""
    source = """func main() -> void { if (x = 1) { return; } }"""
    expected = "Error on line 1 col 28: ="
    assert Parser(source).parse() == expected

def test_094():
    """Test re-declaring same variable in same scope"""
    source = """func main() -> void { let x = 1; let x = 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_095():
    """Test deeply nested return"""
    source = """func deep() -> int { if (true) { if (true) { return 5; } } return 0; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_096():
    """Test semicolon inside expression (should be error)"""
    source = """func main() -> void { let x = 1; x + 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_097():
    """Test identifier with reserved keyword"""
    source = """func main() -> void { let if = 1; }"""
    expected = "Error on line 1 col 26: if"
    assert Parser(source).parse() == expected

def test_098():
    """Test valid while loop with return"""
    source = """func main() -> int { while (false) { return 0; } return 1; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_099():
    """Test unreachable code after return (should be allowed)"""
    source = """func main() -> int { return 1; let x = 2; }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_100():
    """Test unmatched parenthesis in condition"""
    source = """func main() -> void { if ((1 + 2) > 3 { let x = 0; } }"""
    expected = "Error on line 1 col 38: {"
    assert Parser(source).parse() == expected


