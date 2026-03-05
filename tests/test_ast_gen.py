from utils import ASTGenerator
from src.utils.nodes import *

def test_0():
    source = """func f0() -> int { return 0 + 1; }"""
    expected = 'Program(funcs=[FuncDecl(f0, [], int, [ReturnStmt(BinaryOp(IntegerLiteral(0), +, IntegerLiteral(1)))])])'
    assert str(ASTGenerator(source).generate()) == expected


def test_1():
    source = """func f1() -> void { if (1 > 0) { return; } }"""
    expected = "Program(funcs=[FuncDecl(f1, [], void, [IfStmt(BinaryOp(IntegerLiteral(1), >, IntegerLiteral(0)),BlockStmt([ReturnStmt()]),[],None)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_2():
    source = """func f2() -> void { while (x < 2) { x = x + 1; } }"""
    expected = "Program(funcs=[FuncDecl(f2, [], void, [WhileStmt(BinaryOp(Identifier(x), <, IntegerLiteral(2)), BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_3():
    source = """const a = 3 >> f;"""
    expected = "Program(consts=[ConstDecl(a, BinaryOp(IntegerLiteral(3), >>, Identifier(f)))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_4():
    source = """const a = foo(4) + 5;"""
    expected = "Program(consts=[ConstDecl(a, BinaryOp(FunctionCall(Identifier(foo), [IntegerLiteral(4)]), +, IntegerLiteral(5)))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_5():
    source = """const a = foo(9) == 10;"""
    expected = "Program(consts=[ConstDecl(a, BinaryOp(FunctionCall(Identifier(foo), [IntegerLiteral(9)]), ==, IntegerLiteral(10)))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_6():
    source = """const a = foo(19) || 20;"""
    expected = "Program(consts=[ConstDecl(a, BinaryOp(FunctionCall(Identifier(foo), [IntegerLiteral(19)]), ||, IntegerLiteral(20)))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_7():
    source = """func f0() -> void { while (true) { continue; } }"""
    expected = "Program(funcs=[FuncDecl(f0, [], void, [WhileStmt(BooleanLiteral(True), BlockStmt([ContinueStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_8():
    source = """func f2() -> int { return 2; }"""
    expected = "Program(funcs=[FuncDecl(f2, [], int, [ReturnStmt(IntegerLiteral(2))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_9():
    source = """func f3() -> void { a[0] = 3; }"""
    expected = "Program(funcs=[FuncDecl(f3, [], void, [Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(0)), IntegerLiteral(3))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_10():
    source = """func f4() -> void { for (x in a) { print(x); } }"""
    expected = "Program(funcs=[FuncDecl(f4, [], void, [ForStmt(x, Identifier(a), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [Identifier(x)]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected



def test_11():
    source = """func f5() -> void { let x = true; }"""
    expected = "Program(funcs=[FuncDecl(f5, [], void, [VarDecl(x, BooleanLiteral(True))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_12():
    source = """func f6() -> void { while (true) { continue; } }"""
    expected = "Program(funcs=[FuncDecl(f6, [], void, [WhileStmt(BooleanLiteral(True), BlockStmt([ContinueStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_13():
    source = """func f7() -> void { while (true) { break; } }"""
    expected = "Program(funcs=[FuncDecl(f7, [], void, [WhileStmt(BooleanLiteral(True), BlockStmt([BreakStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_14():
    source = """func f8() -> int { return 8; }"""
    expected = "Program(funcs=[FuncDecl(f8, [], int, [ReturnStmt(IntegerLiteral(8))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_15():
    source = """func loop() -> void {
    for (x in arr) {
        break;
    }
}"""
    expected = "Program(funcs=[FuncDecl(loop, [], void, [ForStmt(x, Identifier(arr), BlockStmt([BreakStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_16():
    source = """func add_then_return() -> int {
    let x = 1;
    x = x + 2;
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(add_then_return, [], int, [VarDecl(x, IntegerLiteral(1)), Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(2))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_17():
    source = """func finish() -> void {
    return;
}"""
    expected = "Program(funcs=[FuncDecl(finish, [], void, [ReturnStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_18():
    source = """func nested() -> void {
    while (true) {
        if (input()) {break;}
    }
}"""
    expected = "Program(funcs=[FuncDecl(nested, [], void, [WhileStmt(BooleanLiteral(True), BlockStmt([IfStmt(FunctionCall(Identifier(input), []),BlockStmt([BreakStmt()]),[],None)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_19():
    source = """func greet(name: string) -> string {
    return "Hello, " + name;
}"""
    expected = "Program(funcs=[FuncDecl(greet, [Param(name, string)], string, [ReturnStmt(BinaryOp(StringLiteral('Hello, '), +, Identifier(name)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_20():
    source = """func logic(a: bool, b: bool) -> bool {
    return a || !b;
}"""
    expected = "Program(funcs=[FuncDecl(logic, [Param(a, bool), Param(b, bool)], bool, [ReturnStmt(BinaryOp(Identifier(a), ||, UnaryOp(!, Identifier(b))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_21():
    source = """func count(n: int) -> int {
    if (n <= 0) {return 0;}
    return count(n - 1);
}"""
    expected = "Program(funcs=[FuncDecl(count, [Param(n, int)], int, [IfStmt(BinaryOp(Identifier(n), <=, IntegerLiteral(0)),BlockStmt([ReturnStmt(IntegerLiteral(0))]),[],None), ReturnStmt(FunctionCall(Identifier(count), [BinaryOp(Identifier(n), -, IntegerLiteral(1))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_22():
    source = """func loop() -> void {
    for (x in arr) {
        break;
    }
}"""
    expected = "Program(funcs=[FuncDecl(loop, [], void, [ForStmt(x, Identifier(arr), BlockStmt([BreakStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_23():
    source = """func fill() -> void {
    for (i in range) {
        a[i] = i;
    }
}"""
    expected = "Program(funcs=[FuncDecl(fill, [], void, [ForStmt(i, Identifier(range), BlockStmt([Assignment(ArrayAccessLValue(Identifier(a), Identifier(i)), Identifier(i))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_24():
    source = """func f0(p0: int) -> int {
    let x = a[p0%3];
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(f0, [Param(p0, int)], int, [VarDecl(x, ArrayAccess(Identifier(a), BinaryOp(Identifier(p0), %, IntegerLiteral(3)))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_25():
    source = """func f1(p0: int, p1: int) -> int {
    let x = a[p0%3][p1%3];
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(f1, [Param(p0, int), Param(p1, int)], int, [VarDecl(x, ArrayAccess(ArrayAccess(Identifier(a), BinaryOp(Identifier(p0), %, IntegerLiteral(3))), BinaryOp(Identifier(p1), %, IntegerLiteral(3)))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_26():
    source = """func f2(p0: int, p1: int, p2: int) -> int {
    let x = a[p0%3][p1%3][p2%3];
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(f2, [Param(p0, int), Param(p1, int), Param(p2, int)], int, [VarDecl(x, ArrayAccess(ArrayAccess(ArrayAccess(Identifier(a), BinaryOp(Identifier(p0), %, IntegerLiteral(3))), BinaryOp(Identifier(p1), %, IntegerLiteral(3))), BinaryOp(Identifier(p2), %, IntegerLiteral(3)))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_27():
    source = """func f3(p0: int, p1: int, p2: int, p3: int) -> int {
    let x = a[p0%3];
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(f3, [Param(p0, int), Param(p1, int), Param(p2, int), Param(p3, int)], int, [VarDecl(x, ArrayAccess(Identifier(a), BinaryOp(Identifier(p0), %, IntegerLiteral(3)))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_28():
    source = """func f4(p0: int) -> int {
    let x = a[p0%3][p1%3];
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(f4, [Param(p0, int)], int, [VarDecl(x, ArrayAccess(ArrayAccess(Identifier(a), BinaryOp(Identifier(p0), %, IntegerLiteral(3))), BinaryOp(Identifier(p1), %, IntegerLiteral(3)))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_29():
    source = """func f9(p0: int, p1: int) -> int {
    let x = a[p0%3];
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(f9, [Param(p0, int), Param(p1, int)], int, [VarDecl(x, ArrayAccess(Identifier(a), BinaryOp(Identifier(p0), %, IntegerLiteral(3)))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_30():
    source = """func f0(p0: int) -> int {
    let x = p0 + 0;
}"""
    expected = "Program(funcs=[FuncDecl(f0, [Param(p0, int)], int, [VarDecl(x, BinaryOp(Identifier(p0), +, IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_31():
    source = """func f1(p0: int, p1: int) -> int {
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(f1, [Param(p0, int), Param(p1, int)], int, [ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_32():
    source = """func f2() -> int {
     { continue; }
}"""
    expected = "Program(funcs=[FuncDecl(f2, [], int, [BlockStmt([ContinueStmt()])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_33():
    source = '''
        func foo() -> void {
            a = 1;
        }
    '''
    expected = "Program(funcs=[FuncDecl(foo, [], void, [Assignment(IdLValue(a), IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_34():
    source = """func f4(p0: int) -> int {
 while (x < 100) { x = x + 1; } 
}"""
    expected = "Program(funcs=[FuncDecl(f4, [Param(p0, int)], int, [WhileStmt(BinaryOp(Identifier(x), <, IntegerLiteral(100)), BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_35():
    source = """func f5() -> int {
 for (i in a) { break; } return x;
}"""
    expected = "Program(funcs=[FuncDecl(f5, [], int, [ForStmt(i, Identifier(a), BlockStmt([BreakStmt()])), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_36():
    source = """func f6(p2: int) -> int {
}"""
    expected = "Program(funcs=[FuncDecl(f6, [Param(p2, int)], int, [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_37():
    source = """func f7(p0: int) -> int {
 a[p0 % 2] = x; 
}"""
    expected = "Program(funcs=[FuncDecl(f7, [Param(p0, int)], int, [Assignment(ArrayAccessLValue(Identifier(a), BinaryOp(Identifier(p0), %, IntegerLiteral(2))), Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_38():
    source = """
    func main() -> void {
        (a >> b + c) + a < c;
    }
    """
    expected = "Program(funcs=[FuncDecl(main, [], void, [ExprStmt(BinaryOp(BinaryOp(BinaryOp(Identifier(a), >>, BinaryOp(Identifier(b), +, Identifier(c))), +, Identifier(a)), <, Identifier(c)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_39():
    source = """
    func main() -> int {
        a < c;
    }
    """
    expected = "Program(funcs=[FuncDecl(main, [], int, [ExprStmt(BinaryOp(Identifier(a), <, Identifier(c)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_40():
    source = """
        func foo() -> void {
            if (1) {} else if(2) {} else if(3) {}
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [IfStmt(IntegerLiteral(1),BlockStmt([]),[(IntegerLiteral(2), BlockStmt([])), (IntegerLiteral(3), BlockStmt([]))],None)])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_41():
    source = """
        func foo() -> void {
            if (1) {return;} else if(2) {return;} else if(3) {return;} else {return;}
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [IfStmt(IntegerLiteral(1),BlockStmt([ReturnStmt()]),[(IntegerLiteral(2), BlockStmt([ReturnStmt()])), (IntegerLiteral(3), BlockStmt([ReturnStmt()]))],BlockStmt([ReturnStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_42():
    source = """
        func foo() -> void {
            {
                return;
            }
        }
    """
    expected = "Program(funcs=[FuncDecl(foo, [], void, [BlockStmt([ReturnStmt()])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_44():
    source = """func id(p0: int) -> int { return p0; }"""
    expected = "Program(funcs=[FuncDecl(id, [Param(p0, int)], int, [ReturnStmt(Identifier(p0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_45():
    source = """func arr(p0: int) -> int { let x = a[p0]; return x; }"""
    expected = "Program(funcs=[FuncDecl(arr, [Param(p0, int)], int, [VarDecl(x, ArrayAccess(Identifier(a), Identifier(p0))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_46():
    source = """func cond(p0: int) -> int {
        if (p0 == 0) { return 0; }
        else if (p0 == 1) { return 1; }
        else { return 42; }
    }"""
    expected = "Program(funcs=[FuncDecl(cond, [Param(p0, int)], int, [IfStmt(BinaryOp(Identifier(p0), ==, IntegerLiteral(0)),BlockStmt([ReturnStmt(IntegerLiteral(0))]),[(BinaryOp(Identifier(p0), ==, IntegerLiteral(1)), BlockStmt([ReturnStmt(IntegerLiteral(1))]))],BlockStmt([ReturnStmt(IntegerLiteral(42))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_47():
    source = """func deep(p0: int, p1: int) -> int {
        return a[p0][p1];
    }"""
    expected = "Program(funcs=[FuncDecl(deep, [Param(p0, int), Param(p1, int)], int, [ReturnStmt(ArrayAccess(ArrayAccess(Identifier(a), Identifier(p0)), Identifier(p1)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_48():
    source = """func loop() -> int {
        for (x in a) {
            if (x == 0) { break; }
        }
        return 1;
    }"""
    expected = "Program(funcs=[FuncDecl(loop, [], int, [ForStmt(x, Identifier(a), BlockStmt([IfStmt(BinaryOp(Identifier(x), ==, IntegerLiteral(0)),BlockStmt([BreakStmt()]),[],None)])), ReturnStmt(IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_49():
    source = """func count(p0: int) -> int {
        while (p0 < 10) {
            p0 = p0 + 1;
            continue;
        }
        return p0;
    }"""
    expected = "Program(funcs=[FuncDecl(count, [Param(p0, int)], int, [WhileStmt(BinaryOp(Identifier(p0), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(p0), BinaryOp(Identifier(p0), +, IntegerLiteral(1))), ContinueStmt()])), ReturnStmt(Identifier(p0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_50():
    source = """func nest() -> int {
        {
            let x = 5;
            {
                return x;
            }
        }
    }"""
    expected = "Program(funcs=[FuncDecl(nest, [], int, [BlockStmt([VarDecl(x, IntegerLiteral(5)), BlockStmt([ReturnStmt(Identifier(x))])])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_51():
    source = """func say() -> int {
        let s = "hi";
        return 0;
    }"""
    expected = "Program(funcs=[FuncDecl(say, [], int, [VarDecl(s, StringLiteral('hi')), ReturnStmt(IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_52():
    source = """func pipe(p0: int) -> int {
        return p0 >> double >> triple;
    }"""
    expected = "Program(funcs=[FuncDecl(pipe, [Param(p0, int)], int, [ReturnStmt(BinaryOp(BinaryOp(Identifier(p0), >>, Identifier(double)), >>, Identifier(triple)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_53():
    source = """func arrlit() -> int {
        let a = [[1,2],[3,4]];
        return 1;
    }"""
    expected = "Program(funcs=[FuncDecl(arrlit, [], int, [VarDecl(a, ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])])), ReturnStmt(IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_54():
    source = """const x: int = 5;
func main() -> void {
    print(x);
}"""
    expected = "Program(consts=[ConstDecl(x, int, IntegerLiteral(5))], funcs=[FuncDecl(main, [], void, [ExprStmt(FunctionCall(Identifier(print), [Identifier(x)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_55():
    source = """func check(p0: int) -> int {
    if (p0 > 0) { return 1; }
    return 0;
}"""
    expected = "Program(funcs=[FuncDecl(check, [Param(p0, int)], int, [IfStmt(BinaryOp(Identifier(p0), >, IntegerLiteral(0)),BlockStmt([ReturnStmt(IntegerLiteral(1))]),[],None), ReturnStmt(IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_56():
    source = """func mul(a: int, b: int) -> int {
    return a * b;
}"""
    expected = "Program(funcs=[FuncDecl(mul, [Param(a, int), Param(b, int)], int, [ReturnStmt(BinaryOp(Identifier(a), *, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_57():
    source = """func arr() -> void {
    let x = [1, 2, 3];
}"""
    expected = "Program(funcs=[FuncDecl(arr, [], void, [VarDecl(x, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_58():
    source = """func decl() -> void {
    let a = 1;
    let b = 2;
    let c = a + b;
}"""
    expected = "Program(funcs=[FuncDecl(decl, [], void, [VarDecl(a, IntegerLiteral(1)), VarDecl(b, IntegerLiteral(2)), VarDecl(c, BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_59():
    source = """func greet(name: string) -> string {
    return "Hi, " + name;
}"""
    expected = "Program(funcs=[FuncDecl(greet, [Param(name, string)], string, [ReturnStmt(BinaryOp(StringLiteral('Hi, '), +, Identifier(name)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_60():
    source = """func process(x: int) -> [int; 3] {
    {
        
    }
    {
        let i = "BK";
    }
}"""
    expected = "Program(funcs=[FuncDecl(process, [Param(x, int)], [int; 3], [BlockStmt([]), BlockStmt([VarDecl(i, StringLiteral('BK'))])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_61():
    source = """func seq() -> void {
    print("Start");
    print("Processing");
    print("Done");
}"""
    expected = "Program(funcs=[FuncDecl(seq, [], void, [ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Start')])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Processing')])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Done')]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_62():
    source = """func logic(p: bool, q: bool) -> bool {
    return p && !q;
}"""
    expected = "Program(funcs=[FuncDecl(logic, [Param(p, bool), Param(q, bool)], bool, [ReturnStmt(BinaryOp(Identifier(p), &&, UnaryOp(!, Identifier(q))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_63():
    source = """func set() -> void {
    a[0][1] = 42;
}"""
    expected = "Program(funcs=[FuncDecl(set, [], void, [Assignment(ArrayAccessLValue(ArrayAccess(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(42))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_64():
    source = """func is_positive(n: int) -> bool {
    if (n > 0) { return true; } else { return false; }
}"""
    expected = "Program(funcs=[FuncDecl(is_positive, [Param(n, int)], bool, [IfStmt(BinaryOp(Identifier(n), >, IntegerLiteral(0)),BlockStmt([ReturnStmt(BooleanLiteral(True))]),[],BlockStmt([ReturnStmt(BooleanLiteral(False))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_65():
    source = """func countdown(n: int) -> void {
    while (n > 0 && true) {
        print(str(n));
        n = n - 1;
    }
}"""
    expected = "Program(funcs=[FuncDecl(countdown, [Param(n, int)], void, [WhileStmt(BinaryOp(BinaryOp(Identifier(n), >, IntegerLiteral(0)), &&, BooleanLiteral(True)), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [Identifier(n)])])), Assignment(IdLValue(n), BinaryOp(Identifier(n), -, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_66():
    source = """func greet() -> void {
    say_hello();
}"""
    expected = "Program(funcs=[FuncDecl(greet, [], void, [ExprStmt(FunctionCall(Identifier(say_hello), []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_67():
    source = """func mod3(n: int) -> int {
    return n % 3;
}"""
    expected = "Program(funcs=[FuncDecl(mod3, [Param(n, int)], int, [ReturnStmt(BinaryOp(Identifier(n), %, IntegerLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_68():
    source = """func make_empty() -> void {
    let x: [int; 0] = [];
}"""
    expected = "Program(funcs=[FuncDecl(make_empty, [], void, [VarDecl(x, [int; 0], ArrayLiteral([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_69():
    source = """func math(a: int) -> int {
    return (a + 1) * 2 - 3;
}"""
    expected = "Program(funcs=[FuncDecl(math, [Param(a, int)], int, [ReturnStmt(BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, IntegerLiteral(1)), *, IntegerLiteral(2)), -, IntegerLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_70():
    source = """func literals() -> void {
    let a = 1;
    let b = 2.0;
    let c = true;
    let d = "ok";
}"""
    expected = "Program(funcs=[FuncDecl(literals, [], void, [VarDecl(a, IntegerLiteral(1)), VarDecl(b, FloatLiteral(2.0)), VarDecl(c, BooleanLiteral(True)), VarDecl(d, StringLiteral('ok'))])])"
    assert str(ASTGenerator(source).generate()) == expected



def test_71():
    source = """func get(arr: float, idx: int) -> int {
    return arr[idx + 1];
}"""
    expected = "Program(funcs=[FuncDecl(get, [Param(arr, float), Param(idx, int)], int, [ReturnStmt(ArrayAccess(Identifier(arr), BinaryOp(Identifier(idx), +, IntegerLiteral(1))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_72():
    source = """func loop() -> void {
    for (i in a) {
        while (true) {
            if (i == 0) {continue;}
            break;
        }
    }
}"""
    expected = "Program(funcs=[FuncDecl(loop, [], void, [ForStmt(i, Identifier(a), BlockStmt([WhileStmt(BooleanLiteral(True), BlockStmt([IfStmt(BinaryOp(Identifier(i), ==, IntegerLiteral(0)),BlockStmt([ContinueStmt()]),[],None), BreakStmt()]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_73():
    source = """func check(x: int) -> int {
    if (x < 0){ return -1;}
    if (x == 0){ return 0;}
    return 1;
}"""
    expected = "Program(funcs=[FuncDecl(check, [Param(x, int)], int, [IfStmt(BinaryOp(Identifier(x), <, IntegerLiteral(0)),BlockStmt([ReturnStmt(UnaryOp(-, IntegerLiteral(1)))]),[],None), IfStmt(BinaryOp(Identifier(x), ==, IntegerLiteral(0)),BlockStmt([ReturnStmt(IntegerLiteral(0))]),[],None), ReturnStmt(IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_74():
    source = """func input_and_cast() -> void {
    let x = str(input());
}"""
    expected = "Program(funcs=[FuncDecl(input_and_cast, [], void, [VarDecl(x, FunctionCall(Identifier(str), [FunctionCall(Identifier(input), [])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_75():
    source = """func logic_chain(p: bool, q: bool, r: bool) -> bool {
    return p && q || !r;
}"""
    expected = "Program(funcs=[FuncDecl(logic_chain, [Param(p, bool), Param(q, bool), Param(r, bool)], bool, [ReturnStmt(BinaryOp(BinaryOp(Identifier(p), &&, Identifier(q)), ||, UnaryOp(!, Identifier(r))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_76():
    source = """func nested_calls() -> void {
    print(str(input()));
}"""
    expected = "Program(funcs=[FuncDecl(nested_calls, [], void, [ExprStmt(FunctionCall(Identifier(print), [FunctionCall(Identifier(str), [FunctionCall(Identifier(input), [])])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_77():
    source = """func negate() -> bool {
    return !input();
}"""
    expected = "Program(funcs=[FuncDecl(negate, [], bool, [ReturnStmt(UnaryOp(!, FunctionCall(Identifier(input), [])))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_78():
    source = """func multi_if(x: int) -> int {
    if (x > 10) {
        let y = x * 2;
        return y;
    }
    return 0;
}"""
    expected = "Program(funcs=[FuncDecl(multi_if, [Param(x, int)], int, [IfStmt(BinaryOp(Identifier(x), >, IntegerLiteral(10)),BlockStmt([VarDecl(y, BinaryOp(Identifier(x), *, IntegerLiteral(2))), ReturnStmt(Identifier(y))]),[],None), ReturnStmt(IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_79():
    source = """func log() -> void {
    print("Start  comment");
    print("End comment */");
}"""
    expected = "Program(funcs=[FuncDecl(log, [], void, [ExprStmt(FunctionCall(Identifier(print), [StringLiteral('Start  comment')])), ExprStmt(FunctionCall(Identifier(print), [StringLiteral('End comment */')]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_80():
    source = """func square(x: int) -> int {
    return pow(x, 2);
}"""
    expected = "Program(funcs=[FuncDecl(square, [Param(x, int)], int, [ReturnStmt(FunctionCall(Identifier(pow), [Identifier(x), IntegerLiteral(2)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_81():
    source = """func assign_and_return(x: int) -> int {
    x = x + 1;
    return x;
}"""
    expected = "Program(funcs=[FuncDecl(assign_and_return, [Param(x, int)], int, [Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1))), ReturnStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_82():
    source = """func dyn_array(n: int) -> void {
    let arr: [int; 5] = [1,2,3,4,5];
}"""
    expected = "Program(funcs=[FuncDecl(dyn_array, [Param(n, int)], void, [VarDecl(arr, [int; 5], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_83():
    source = """func nested_return() -> int {
    {
        {
            return 123;
        }
    }
}"""
    expected = "Program(funcs=[FuncDecl(nested_return, [], int, [BlockStmt([BlockStmt([ReturnStmt(IntegerLiteral(123))])])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_84():
    source = """func calc() -> int {
    return (1 + 2) * (3 - 4);
}"""
    expected = "Program(funcs=[FuncDecl(calc, [], int, [ReturnStmt(BinaryOp(BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)), *, BinaryOp(IntegerLiteral(3), -, IntegerLiteral(4))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_85():
    source = """func update(i: int) -> void {
    a[i + 1] = 5;
}"""
    expected = "Program(funcs=[FuncDecl(update, [Param(i, int)], void, [Assignment(ArrayAccessLValue(Identifier(a), BinaryOp(Identifier(i), +, IntegerLiteral(1))), IntegerLiteral(5))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_86():
    source = """func callarr() -> void {
    use(1,2,3);
}"""
    expected = "Program(funcs=[FuncDecl(callarr, [], void, [ExprStmt(FunctionCall(Identifier(use), [IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_87():
    source = """func testfloat() -> void {
    let pi = 3.14 * 2.0;
}"""
    expected = "Program(funcs=[FuncDecl(testfloat, [], void, [VarDecl(pi, BinaryOp(FloatLiteral(3.14), *, FloatLiteral(2.0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_88():
    source = """func mix() -> void {
    let a = 1;
    let b = "hi";
    let c = true;
}"""
    expected = "Program(funcs=[FuncDecl(mix, [], void, [VarDecl(a, IntegerLiteral(1)), VarDecl(b, StringLiteral('hi')), VarDecl(c, BooleanLiteral(True))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_89():
    source = """func nested() -> int {
    return f1(f2(3));
}"""
    expected = "Program(funcs=[FuncDecl(nested, [], int, [ReturnStmt(FunctionCall(Identifier(f1), [FunctionCall(Identifier(f2), [IntegerLiteral(3)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_90():
    source = """func chain() -> void {
    result = f1(f2(f3()));
}"""
    expected = "Program(funcs=[FuncDecl(chain, [], void, [Assignment(IdLValue(result), FunctionCall(Identifier(f1), [FunctionCall(Identifier(f2), [FunctionCall(Identifier(f3), [])])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_91():
    source = """func reorder() -> void {
    x = y;
    let y = 1;
}"""
    expected = "Program(funcs=[FuncDecl(reorder, [], void, [Assignment(IdLValue(x), Identifier(y)), VarDecl(y, IntegerLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_92():
    source = """func f1() -> int { return 1; }
func f2() -> int { return 2; }"""
    expected = "Program(funcs=[FuncDecl(f1, [], int, [ReturnStmt(IntegerLiteral(1))]), FuncDecl(f2, [], int, [ReturnStmt(IntegerLiteral(2))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_93():
    source = """func recurse(n: int) -> int {
    if (n <= 0) {return 0;}
    return n + recurse(n - 1);
}"""
    expected = "Program(funcs=[FuncDecl(recurse, [Param(n, int)], int, [IfStmt(BinaryOp(Identifier(n), <=, IntegerLiteral(0)),BlockStmt([ReturnStmt(IntegerLiteral(0))]),[],None), ReturnStmt(BinaryOp(Identifier(n), +, FunctionCall(Identifier(recurse), [BinaryOp(Identifier(n), -, IntegerLiteral(1))])))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_94():
    source = """func equal(a: int, b: int) -> bool {
    return a == b;
}"""
    expected = "Program(funcs=[FuncDecl(equal, [Param(a, int), Param(b, int)], bool, [ReturnStmt(BinaryOp(Identifier(a), ==, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_95():
    source = """func early(x: int) -> int {
    if (x == 1) {return 100;}
    return 0;
}"""
    expected = "Program(funcs=[FuncDecl(early, [Param(x, int)], int, [IfStmt(BinaryOp(Identifier(x), ==, IntegerLiteral(1)),BlockStmt([ReturnStmt(IntegerLiteral(100))]),[],None), ReturnStmt(IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_96():
    source = """func divide(a: float, b: float) -> float {
    return a / b;
}"""
    expected = "Program(funcs=[FuncDecl(divide, [Param(a, float), Param(b, float)], float, [ReturnStmt(BinaryOp(Identifier(a), /, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_97():
    source = """func chain(p: bool, q: bool) -> bool {
    return (p || q) && true;
}"""
    expected = "Program(funcs=[FuncDecl(chain, [Param(p, bool), Param(q, bool)], bool, [ReturnStmt(BinaryOp(BinaryOp(Identifier(p), ||, Identifier(q)), &&, BooleanLiteral(True)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_98():
    source = """func neg(x: int) -> int {
    return -x;
}"""
    expected = "Program(funcs=[FuncDecl(neg, [Param(x, int)], int, [ReturnStmt(UnaryOp(-, Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_99():
    source = """func nestarr() -> void {
    let a = [[1],[2,3]];
}"""
    expected = "Program(funcs=[FuncDecl(nestarr, [], void, [VarDecl(a, ArrayLiteral([ArrayLiteral([IntegerLiteral(1)]), ArrayLiteral([IntegerLiteral(2), IntegerLiteral(3)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_100():
    source = """func format(x: int) -> void {
    let s = str(x);
}"""
    expected = "Program(funcs=[FuncDecl(format, [Param(x, int)], void, [VarDecl(s, FunctionCall(Identifier(str), [Identifier(x)]))])])"
    assert str(ASTGenerator(source).generate()) == expected
def test_006():
        source = """
    func main() -> void {
        let x = y;
    }
    """
        expected = "Undeclared Identifier: y"
        assert str(ASTGenerator(source).generate()) == expected
def test_008():
        source = """
    func main() -> void {
        let x = input();
        let y = input1();
    }
    """
        expected = "Undeclared Function: input1"
        assert str(ASTGenerator(source).generate()) == expected
    
def test_007():
        source = """
    func foo() -> void {}
    func main() -> void {
        foo();
        goo();
    }
    """
        expected = "Undeclared Function: input1"

        assert str(ASTGenerator(source).generate()) == expected

def test_086():
        source = """
    const array = [[1], [2]];
    func main() -> void {
        for (a in array) {
            a = [2];
            a = [1,2];
        }
    }
    """
        expected = "Undeclared Function: input1"

        assert str(ASTGenerator(source).generate()) == expected
def test_092():
        source = """
    func main() -> void {
        if (true) {
            return;
            return 1;
        }
    }
    """
        expected = "Undeclared Function: input1"

        assert str(ASTGenerator(source).generate()) == expected
def test_094():
        source = """
    func main() -> void {
        if (true) {return;}
        else if (true) {return;}
        else if (true) {return 1;}
        else {return;}
    }
    """
        expected = "Undeclared Function: input1"

        assert str(ASTGenerator(source).generate()) == expected
def test_130():
        source = """
    func main() -> void {
        let a = [[1, 2], [3, 4]];
        let c: [int; 2] = a[1];
        let d: int = a[1][--2];
        c = a[1][2];
    }
    """
        expected = "Undeclared Function: input1"

        assert str(ASTGenerator(source).generate()) == expected
def test_210():
        source = """
    func foo(a: [[[[[int; 2]; 2]; 2]; 2]; 2]) -> void {
        a[0][1][2][3][4] = 2;
    }
    func main() -> void {
    
    }
    """
        expected = "Undeclared Function: input1"

        assert str(ASTGenerator(source).generate()) == expected