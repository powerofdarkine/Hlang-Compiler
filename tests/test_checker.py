from utils import Checker
from src.semantics.static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)
from src.utils.nodes import *
def test1():
    source = """
    func compute() -> int {
        let x: int = 5;
        return 1;
    }
    func main() -> void {}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test2():
    source = """
    func compute() -> string {
        return 10;
    }
    func main() -> void {}
    """
    expected = TypeMismatchInStatement(ReturnStmt(IntegerLiteral(10)))
    assert Checker(source).check_from_source() == str(expected)


def test3():
    source = """
    func main() -> void {
        let a: [int; 2] = [1, 2];
        a = [1, 2, 3];
    }
    """
    expected = TypeMismatchInStatement(Assignment(IdLValue("a"), ArrayLiteral([
        IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)
    ])))
    assert Checker(source).check_from_source() == str(expected)


def test4():
    source = """
    func greet(name: string) -> void {
        print(name);
    }
    func main() -> void {
        greet();
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(greet), []))"
    assert Checker(source).check_from_source() == expected


def test5():
    source = """
    func main() -> void {
        if ("hello") {
            print("bad");
        }
    }
    """
    expected = TypeMismatchInStatement(IfStmt(
        StringLiteral("hello"),
        BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("bad")]))]),
        [],
        None
    ))
    assert Checker(source).check_from_source() == str(expected)


def test6():
    source = """
    func main() -> void {
        let i: int = 5;
        for (i in [1, 2, 3]) {
            print(i);
        }
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(print), [Identifier(i)]))"
    assert Checker(source).check_from_source() == expected


def test7():
    source = """
    const PI: float = 3.14;
    func main() -> void {
        PI = 3.1415;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(PI), FloatLiteral(3.1415))"
    assert Checker(source).check_from_source() == expected


def test8():
    source = """
    func log() -> void {
        print("log");
    }
    func main() -> void {
        let x = log();
    }
    """
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(log), [])"
    assert Checker(source).check_from_source() == expected


def test9():
    source = """
    func main() -> void {
        let a: [int; 2] = [1, 2];
        let b = a[1];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test10():
    source = """
    func inner() -> void {}
    func inner() -> void {}
    func main() -> void {
        
    }
    """
    expected = "Redeclared Function: inner"
    assert Checker(source).check_from_source() == expected


def test11():
    source = """
    func main() -> void {
        let arr: [int; 2] = [1, 2];
        arr = [1];
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(arr), ArrayLiteral([IntegerLiteral(1)]))"
    assert Checker(source).check_from_source() == expected


def test12():
    source = """
    func main() -> void {
        let a: bool = 1 && "true";
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), &&, StringLiteral('true'))"
    assert Checker(source).check_from_source() == expected


def test13():
    source = """
    func main() -> void {
        return 1;
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test14():
    source = """
    func main() -> void {
        continue;
    }
    """
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected


def test15():
    source = """
    func sum(a: int, b: int) -> int {
        return a + b;
    }
    func sum(a: float, b: float) -> float {
        return a + b;
    }
    func main() -> void {}
    """
    expected = "Redeclared Function: sum"
    assert Checker(source).check_from_source() == expected


def test16():
    source = """
    func add(a: int) -> int {
        return a;
    }
    func main() -> void {
        let x = add(1, 2);
    }
    """
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(1), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == expected


def test17():
    source = """
    func main() -> void {
        let s: string = 1 + "world";
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), +, StringLiteral('world'))"
    assert Checker(source).check_from_source() == expected


def test18():
    source = """
    func main() -> void {
        let arr = [1, 2];
        arr[0] = "string";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), StringLiteral('string'))"
    assert Checker(source).check_from_source() == expected


def test19():
    source = """
    func printer() -> void {
        print("ok");
    }
    func main() -> void {
        let x = printer();
    }
    """
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(printer), [])"
    assert Checker(source).check_from_source() == expected


def test20():
    source = """
    func toInt(s: string) -> int {
        return 1;
    }
    func main() -> void {
        let a: bool = toInt("10");
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(a, bool, FunctionCall(Identifier(toInt), [StringLiteral('10')]))"
    assert Checker(source).check_from_source() == expected


def test21():
    source = """
    func main() -> void {
        let a: [[int; 2]; 2] = [[1, 2], [3]];
    }
    """
    expected = "Type Mismatch In Expression: ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3)])])"
    assert Checker(source).check_from_source() == expected


def test22():
    source = """
    func main() -> void {
        let a = true + 1;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), +, IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test23():
    source = """
    func log() -> void {
        print("ok");
    }
    func main() -> void {
        let a = log() + 1;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(FunctionCall(Identifier(log), []), +, IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test24():
    source = """
    func greet(a: string) -> void {
        print(a);
    }
    func main() -> void {
        greet(1);
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(greet), [IntegerLiteral(1)]))"
    assert Checker(source).check_from_source() == expected


def test25():
    source = """
    func compute() -> int {
        return "abc";
    }
    func main() -> void {}
    """
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('abc'))"
    assert Checker(source).check_from_source() == expected


def test26():
    source = """
    const a: int = 5;
    func main() -> void {
        a = 10;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), IntegerLiteral(10))"
    assert Checker(source).check_from_source() == expected


def test27():
    source = """
    func main() -> void {
        return;
        return;
        return 1;
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test28():
    source = """
    func main() -> void {
        let arr: [int; 2] = [1, 2];
        let x = arr[0];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test29():
    source = """
    func add(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        let x = add(1);
    }
    """
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(1)])"
    assert Checker(source).check_from_source() == expected


def test30():
    source = """
    func main() -> void {
        let arr = [1, 2];
        arr[0][1] = 3;
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccessLValue(ArrayAccess(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected
def test31():
    source = """
    func main() -> void {
        let x = 5;
        x = "string";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(x), StringLiteral('string'))"
    assert Checker(source).check_from_source() == expected


def test32():
    source = """
    func main() -> void {
        let arr = [1, 2];
        let x = arr["0"];
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), StringLiteral('0'))"
    assert Checker(source).check_from_source() == expected


def test33():
    source = """
    func main() -> void {
        let x: int = y;
    }
    """
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected


def test34():
    source = """
    func main() -> void {
        break;
    }
    """
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


def test35():
    source = """
    func log() -> void {
        print("log");
    }
    func main() -> void {
        log = 5;
    }
    """
    expected = "Undeclared Identifier: log"
    assert Checker(source).check_from_source() == expected


def test36():
    source = """
    func main() -> void {
        let arr: [[int; 2]; 2] = [[1, 2], [3, 4, 5]];
    }
    """
    expected = "Type Mismatch In Expression: ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])])"
    assert Checker(source).check_from_source() == expected


def test37():
    source = """
    func doSomething() -> void {
        return 1;
    }
    func main() -> void {}
    """
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test38():
    source = """
    func main() -> void {
        for (i in [1, 2]) {
            if (true) {
                continue;
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test39():
    source = """
    func main() -> void {
        10 == 5;
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(BinaryOp(IntegerLiteral(10), ==, IntegerLiteral(5)))"
    assert Checker(source).check_from_source() == expected


def test40():
    source = """
    func main() -> void {
        let x: int = 5;
        let x: string = "hi";
    }
    """
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected
def test41():
    source = """
    func main() -> void {
        let x: bool = true;
        x = 0;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(x), IntegerLiteral(0))"
    assert Checker(source).check_from_source() == expected


def test42():
    source = """
    func main() -> void {
        let x: float = 2.5;
        x = "2.5";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(x), StringLiteral('2.5'))"
    assert Checker(source).check_from_source() == expected


def test43():
    source = """
    func get() -> int {
        return 1;
    }
    func main() -> void {
        let a: string = get();
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(a, string, FunctionCall(Identifier(get), []))"
    assert Checker(source).check_from_source() == expected


def test44():
    source = """
    func main() -> void {
        let a: [int; 2] = [1, "two"];
    }
    """
    expected = "Type Mismatch In Expression: ArrayLiteral([IntegerLiteral(1), StringLiteral('two')])"
    assert Checker(source).check_from_source() == expected


def test45():
    source = """
    func main() -> void {
        let x: int = 10;
        x = x + true;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(x), +, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test46():
    source = """
    func main() -> void {
        let x = 1;
        let x = "shadow";
    }
    """
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected


def test47():
    source = """
    func foo() -> int {
        let x: int = 5;
        return x;
    }
    func main() -> void {}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test48():
    source = """
    func main() -> void {
        for (x in [10]) {
            print("hello");
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test49():
    source = """
    func main() -> void {
        let arr = [1, 2];
        let x = arr[0];
        print("x");
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test50():
    source = """
    func main() -> void {
        let arr: [string; 2] = ["a", "b"];
        arr[1] = 1;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(1)), IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected
def test51():
    source = """
    func main() -> void {
        let arr: [[int; 2]; 2] = [[1, 2], [3, 4]];
        let x = arr[1][1];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test52():
    source = """
    func main() -> void {
        let arr: [[int; 2]; 3] = [[1, 2], [3, 4]];
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(arr, [[int; 2]; 3], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])]))"
    assert Checker(source).check_from_source() == expected


def test53():
    source = """
    func main() -> void {
        let a: bool = !false;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test54():
    source = """
    func main() -> void {
        let a = true || "false";
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), ||, StringLiteral('false'))"
    assert Checker(source).check_from_source() == expected


def test55():
    source = """
    func main() -> void {
        let arr: [int; 2] = [1, 2];
        let x = arr[2];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected  # Out-of-bounds is usually a runtime error


def test56():
    source = """
    func main() -> void {
        let a = 1 ;
        a = "oops";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), StringLiteral('oops'))"
    assert Checker(source).check_from_source() == expected


def test57():
    source = """
    func add(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        let x: float = add(1, 2);
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(x, float, FunctionCall(Identifier(add), [IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected


def test58():
    source = """
    func main() -> void {
        let s = "hi" + "3.5";
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test59():
    source = """
    func main() -> void {
        let a: [int; 2] = [1, 2];
        a[0] = "x";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(0)), StringLiteral('x'))"
    assert Checker(source).check_from_source() == expected


def test60():
    source = """
    func inc(x: int) -> int {
        return x + 1;
    }
    func main() -> void {
        let result = inc(5);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test61():
    source = """
    func main() -> void {
        let x = 5;
        {
            let x = "string";
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test62():
    source = """
    func main() -> void {
        let x: [int; 3] = [1, 2];
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(x, [int; 3], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected


def test63():
    source = """
    func main() -> void {
        let x = [1, 2];
        let y = x[0] + x[1];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test64():
    source = """
    func getValue() -> int {
        return 5;
    }
    func main() -> void {
        let x: string = getValue();
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(x, string, FunctionCall(Identifier(getValue), []))"
    assert Checker(source).check_from_source() == expected


def test65():
    source = """
    func printStr(s: string) -> void {
        print(s);
    }
    func main() -> void {
        printStr("Hello");
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test66():
    source = """
    func main() -> void {
        let arr = [[1, 2], [3, 4]];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test67():
    source = """
    func f() -> int {
        let x: int = 5;
        return;
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt()"
    assert Checker(source).check_from_source() == expected


def test68():
    source = """
    func f(x: int) -> int {
        return x;
    }
    func main() -> void {
        let x = f("abc");
    }
    """
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(f), [StringLiteral('abc')])"
    assert Checker(source).check_from_source() == expected


def test69():
    source = """
    func main() -> void {
        let flag: bool = true;
        if (flag) {
            print("ok");
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test70():
    source = """
    func main() -> void {
        let a: int = 1;
        let b: string = "hi";
        let c = a + b;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(a), +, Identifier(b))"
    assert Checker(source).check_from_source() == expected
def test71():
    source = """
    func main() -> void {
        let a: int = 1;
        let b: int = 2;
        let c = a + b;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test72():
    source = """
    func main() -> void {
        let x: [float; 2] = [1.0, 2];
    }
    """
    expected = "Type Mismatch In Expression: ArrayLiteral([FloatLiteral(1.0), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == expected


def test73():
    source = """
    func main() -> void {
        let s: string = "a" + "lllll";
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test74():
    source = """
    func main() -> void {
        let x: bool = 1 < "2";
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), <, StringLiteral('2'))"
    assert Checker(source).check_from_source() == expected


def test75():
    source = """
    func main() -> void {
        let a: int = 1;
        let b: float = 2.5;
        let c = a + b;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test76():
    source = """
    func main() -> void {
        let flag = true;
        if (flag) {
            let msg = "ok";
            print(msg);
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test77():
    source = """
    func compute() -> bool {
        return 1 + 2;
    }
    func main() -> void {}
    """
    expected = "Type Mismatch In Statement: ReturnStmt(BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)))"
    assert Checker(source).check_from_source() == expected


def test78():
    source = """
    func main() -> void {
        let a: [int; 2] = [1, 2];
        let b = a[0][1];
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccess(ArrayAccess(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test79():
    source = """
    func main() -> void {
        let arr = [1, 2];
        arr[true] = 0;
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccessLValue(Identifier(arr), BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test80():
    source = """
    func main() -> void {
        let a: int = 1;
        let b: string = "x";
        a = b;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), Identifier(b))"
    assert Checker(source).check_from_source() == expected
def test81():
    source = """
    func main() -> void {
        let a: int = 5;
        let b: int = 10;
        if (a + b) {
            print("sum");
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(condition=BinaryOp(Identifier(a), +, Identifier(b)), then_stmt=BlockStmt([ExprStmt(FunctionCall(Identifier(print), [StringLiteral('sum')]))]))"
    assert Checker(source).check_from_source() == expected


def test82():
    source = """
    func main() -> void {
        let a = 5 + true;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), +, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test83():
    source = """
    func f(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        let x = f(1, 2, 3);
    }
    """
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(f), [IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])"
    assert Checker(source).check_from_source() == expected


def test84():
    source = """
    func main() -> void {
        let a: string = "abc";
        a = 1 + 2;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), BinaryOp(IntegerLiteral(1), +, IntegerLiteral(2)))"
    assert Checker(source).check_from_source() == expected


def test85():
    source = """
    func test() -> void {
        return 1;
    }
    func main() -> void {}
    """
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test86():
    source = """
    func main() -> void {
        let a: [string; 2] = ["a", "b"];
        a[0] = 1;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test87():
    source = """
    func main() -> void {
        let x: int = true;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(x, int, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test88():
    source = """
    func inc(x: int) -> int {
        return x + 1;
    }
    func main() -> void {
        let a = inc(1);
        let b: string = a;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(b, string, Identifier(a))"
    assert Checker(source).check_from_source() == expected


def test89():
    source = """
    func main() -> void {
        let arr = [1, 2];
        arr["0"] = 3;
        
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccessLValue(Identifier(arr), StringLiteral('0'))"
    assert Checker(source).check_from_source() == expected


def test90():
    source = """
    func main() -> void {
        let a: int = 1;
        let b: int = 2;
        let c: string = a < b;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(c, string, BinaryOp(Identifier(a), <, Identifier(b)))"
    assert Checker(source).check_from_source() == expected
def test91():
    source = """
    func main() -> void {
        let a: int = 1;
        let b = a && true;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(Identifier(a), &&, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected


def test92():
    source = """
    func main() -> void {
        let x: int = 1;
        let y: float = 1.0;
        let z = x * y;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test93():
    source = """
    func main() -> void {
        let a: [int; 2] = [1, 2];
        let b = a[1.0];
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(a), FloatLiteral(1.0))"
    assert Checker(source).check_from_source() == expected


def test94():
    source = """
    func main() -> void {
        let a: [int; 2] = [1, 2];
        a[0][1] = 3;
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccessLValue(ArrayAccess(Identifier(a), IntegerLiteral(0)), IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected


def test95():
    source = """
    func main() -> void {
        let s: string = "a" + "b";
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test96():
    source = """
    func main() -> void {
        let x: string = "hello";
        let y = x + 1;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test97():
    source = """
    const a: int = 1;
    func main() -> void {
        a = 2;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), IntegerLiteral(2))"
    assert Checker(source).check_from_source() == expected


def test98():
    source = """
    func getValue() -> float {
        return 3.14;
    }
    func main() -> void {
        let a: int = getValue();
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(a, int, FunctionCall(Identifier(getValue), []))"
    assert Checker(source).check_from_source() == expected


def test99():
    source = """
    func main() -> void {
        let a = 1 < 2;
        let b: string = a;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(b, string, Identifier(a))"
    assert Checker(source).check_from_source() == expected


def test100():
    source = """
    func add(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        let result = add(1, 2);
        print("o");
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
def test_0043():
        source = """
    const a = goo();
    func foo() -> void {}
    func goo() -> int {return 1;}
    func main() -> void {}
    """
        expected = "Undeclared Function: goo"
        assert Checker(source).check_from_source() == str(expected)