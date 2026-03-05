from src.utils.nodes import *
from utils import CodeGenerator

def test_001():
    source = """
    func main() -> void {
        print("Hello World");
    }
    """
    expected = "Hello World"
    assert CodeGenerator().generate_and_run(source) == expected

def test_002():
    source = """
    func main() -> void {
        print(int2str(42));
    }
    """
    expected = "42"
    assert CodeGenerator().generate_and_run(source) == expected

def test_003():
    source = """
    func main() -> void {
        let a: int = 5 + 3;
        print(int2str(a));
    }
    """
    expected = "8"
    assert CodeGenerator().generate_and_run(source) == expected

def test_004():
    source = """
    func main() -> void {
        let b: float = 3.5 + 1.5;
        print(float2str(b));
    }
    """
    expected = "5.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_005():
    source = """
    func main() -> void {
        let s: string = "foo" + "bar";
        print(s);
    }
    """
    expected = "foobar"
    assert CodeGenerator().generate_and_run(source) == expected

def test_006():
    source = """
    func main() -> void {
        print(bool2str(2 > 1));
    }
    """
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_007():
    source = """
    func main() -> void {
        let arr: [int; 3] = [10, 20, 30];
        print(int2str(arr[1]));
    }
    """
    expected = "20"
    assert CodeGenerator().generate_and_run(source) == expected

def test_008():
    source = """
    func add(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        print(int2str(add(4, 5)));
    }
    """
    expected = "9"
    assert CodeGenerator().generate_and_run(source) == expected

def test_009():
    source = """
    func main() -> void {
        let i: float = 7.0 - 2;
        print(float2str(i));
    }
    """
    expected = "5.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_010():
    source = """
    func main() -> void {
        if (false) { print("A"); }
        else { print("B"); }
    }
    """
    expected = "B"
    assert CodeGenerator().generate_and_run(source) == expected
def test_011():
    source = """
    func main() -> void {
        let a: int = 10 / 3;
        print(int2str(a));
    }
    """
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_012():
    source = """
    func main() -> void {
        let b: int = 10 / 4;
        print(int2str(b));
    }
    """
    expected = "2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_013():
    source = """
    func main() -> void {
        let s: string = "abc";
        print(s + int2str(123));
    }
    """
    expected = "abc123"
    assert CodeGenerator().generate_and_run(source) == expected

def test_014():
    source = """
    func main() -> void {
        print(bool2str(5 == 5));
    }
    """
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_015():
    source = """
    func main() -> void {
        let arr: [string; 2] = ["hi", "bye"];
        print(arr[0]);
        print(arr[1]);
    }
    """
    expected = "hi\nbye"
    assert CodeGenerator().generate_and_run(source) == expected

def test_016():
    source = """
    func mult(a: int, b: int) -> int {
        return a * b;
    }
    func main() -> void {
        print(int2str(mult(6, 7)));
    }
    """
    expected = "42"
    assert CodeGenerator().generate_and_run(source) == expected

def test_017():
    source = """
    func main() -> void {
        let f: bool = !true;
        print(bool2str(f));
    }
    """
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_018():
    source = """
    func main() -> void {
        let i: int = 0;
        while (i < 3) {
            print(int2str(i));
            i = i + 1;
        }
    }
    """
    expected = "0\n1\n2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_019():
    source = """
    func main() -> void {
        let arr: [int; 2] = [2, 4];
        arr[1] = arr[1] + arr[0];
        print(int2str(arr[1]));
    }
    """
    expected = "6"
    assert CodeGenerator().generate_and_run(source) == expected

def test_020():
    source = """
    func main() -> void {
        if (1 > 2) { print("no"); }
        else if (2 > 3) { print("still no"); }
        else { print("yes"); }
    }
    """
    expected = "yes"
    assert CodeGenerator().generate_and_run(source) == expected
def test_021():
    source = """
    func main() -> void {
        let a: [float; 3] = [1.0, 2.5, 3.5];
        print(float2str(a[0] + a[1] + a[2]));
    }
    """
    expected = "7.0"
    assert CodeGenerator().generate_and_run(source) == expected

def test_022():
    source = """
    func main() -> void {
        print(bool2str("abc" != "def"));
    }
    """
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_023():
    source = """
    func main() -> void {
        let a: [[int; 2]; 2] = [[1, 2], [3, 4]];
        print(int2str(a[0][0] + a[1][1]));
    }
    """
    expected = "5"
    assert CodeGenerator().generate_and_run(source) == expected

def test_024():
    source = """
    func sum(a: int, b: int) -> int {
        return a + b;
    }
    func main() -> void {
        if (sum(2, 3) == 5) { print("ok"); }
        else { print("fail"); }
    }
    """
    expected = "ok"
    assert CodeGenerator().generate_and_run(source) == expected

def test_025():
    source = """
    func main() -> void {
        let i = 1;
        let j = 2;
        print(int2str((i + j) * (j - i)));
    }
    """
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_026():
    source = """
    func main() -> void {
        let s = "";
        for (x in [1, 2, 3]) {
            s = s + int2str(x);
        }
        print(s);
    }
    """
    expected = "123"
    assert CodeGenerator().generate_and_run(source) == expected

def test_027():
    source = """
    func square(n: int) -> int { return n * n; }
    func main() -> void {
        print(int2str(square(5)));
    }
    """
    expected = "25"
    assert CodeGenerator().generate_and_run(source) == expected

def test_028():
    source = """
    func main() -> void {
        let arr: [bool; 3] = [true, false, true];
        print(bool2str(arr[0] || arr[2]));
    }
    """
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_029():
    source = """
    func main() -> void {
        let n = 3;
        while (n > 0) {
            print(int2str(n));
            n = n - 1;
        }
    }
    """
    expected = "3\n2\n1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_030():
    source = """
    func main() -> void {
        let a = 2;
        let b = 3;
        if ((a * b) % 2 == 0) { print("even"); }
        else { print("odd"); }
    }
    """
    expected = "even"
    assert CodeGenerator().generate_and_run(source) == expected
def test_031():
    source = """
    func main() -> void {
        print(bool2str(!false));
    }
    """
    expected = "true"
    assert CodeGenerator().generate_and_run(source) == expected

def test_032():
    source = """
    func main() -> void {
        let a = 5;
        let b = 10;
        let c = a;
        a = b;
        b = c;
        print(int2str(a));
        print(int2str(b));
    }
    """
    expected = "10\n5"
    assert CodeGenerator().generate_and_run(source) == expected

def test_033():
    source = """
    func main() -> void {
        let arr: [int; 4] = [1, 2, 3, 4];
        arr[2] = arr[2] + arr[0];
        print(int2str(arr[2]));
    }
    """
    expected = "4"
    assert CodeGenerator().generate_and_run(source) == expected

def test_034():
    source = """
    func main() -> void {
        let s = "" + true + 1 + 2.5 + "x";
        print(s);
    }
    """
    expected = "true12.5x"
    assert CodeGenerator().generate_and_run(source) == expected

def test_035():
    source = """
    func main() -> void {
        let i = 0;
        while (i < 3) {
            print(int2str(i));
            i = i + 2;
        }
    }
    """
    expected = "0\n2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_036():
    source = """
    func main() -> void {
        let arr: [[string; 2]; 2] = [["a", "b"], ["c", "d"]];
        print(arr[1][0] + arr[0][1]);
    }
    """
    expected = "cb"
    assert CodeGenerator().generate_and_run(source) == expected

def test_037():
    source = """
    func id(x: int) -> int { return x; }
    func main() -> void {
        print(int2str(id(id(7))));
    }
    """
    expected = "7"
    assert CodeGenerator().generate_and_run(source) == expected

def test_038():
    source = """
    func main() -> void {
        let a = 1;
        {
            let a = 99;
            print(int2str(a));
        }
        print(int2str(a));
    }
    """
    expected = "99\n1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_039():
    source = """
    func main() -> void {
        let x = 5;
        if (x < 5) { print("less"); }
        else if (x > 5) { print("more"); }
        else { print("equal"); }
    }
    """
    expected = "equal"
    assert CodeGenerator().generate_and_run(source) == expected

def test_040():
    source = """
    func main() -> void {
        let sum = 0;
        for (n in [1, 2, 3, 4]) {
            sum = sum + n;
        }
        print(int2str(sum));
    }
    """
    expected = "10"
    assert CodeGenerator().generate_and_run(source) == expected
def test_041():
    source = """
    func main() -> void {
        let arr: [int; 3] = [1, 2, 3];
        print(int2str(len(arr)));
    }
    """
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_042():
    source = """
    func main() -> void {
        let arr: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];
        print(int2str(len(arr)));
        print(int2str(len(arr[0])));
    }
    """
    expected = "3\n2"
    assert CodeGenerator().generate_and_run(source) == expected

def test_043():
    source = """
    func main() -> void {
        print("s" + 1);
        print("s" + 1.0);
        print("s" + true);
        print("s" + "s");
    }
    """
    expected = "s1\ns1.0\nstrue\nss"
    assert CodeGenerator().generate_and_run(source) == expected

def test_044():
    source = """
    func main() -> void {
        let a: [int; 3] = [1, 2, 3];
        a[1] = 5;
        print(int2str(a[0]));
        print(int2str(a[1]));
        print(int2str(a[2]));
    }
    """
    expected = "1\n5\n3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_045():
    source = """
    func main() -> void {
        let a: [int; 5] = [1, 2, 3, 4, 5];
        a[a[a[a[0]]]] = a[a[a[a[1]]]];
        print(int2str(a[3]));
    }
    """
    expected = "5"
    assert CodeGenerator().generate_and_run(source) == expected

def test_046():
    source = """
    func foo(a: bool, b: float, c: string) -> void {
        print("" + a + b + c);
    }
    func main() -> void {
        foo(true, 1.0, "s");
    }
    """
    expected = "true1.0s"
    assert CodeGenerator().generate_and_run(source) == expected

def test_047():
    source = """
    func foo() -> int {
        return 1;
    }
    func main() -> void {
        print("" + foo());
    }
    """
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_048():
    source = """
    const a = 1;
    func main() -> void {
        print("" + a);
    }
    """
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_049():
    source = """
    const a = [1, 2, 3];
    const b = a[a[1]];
    func main() -> void {
        print("" + b);
    }
    """
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_050():
    source = """
    func foo1() -> bool { return true; }
    func foo2() -> float { return 1.2; }
    func foo3() -> string { return "s"; }
    func main() -> void {
        print("" + foo1() + foo2() + foo3());
    }
    """
    expected = "true1.2s"
    assert CodeGenerator().generate_and_run(source) == expected
def test_051():
    source = """
    func main() -> void {
        let i = 0;
        while (i < 5) {
            if (i == 3) {break;}
            print("" + i);
            i = i + 1;
        }
    }
    """
    expected = "0\n1\n2"
    assert CodeGenerator().generate_and_run(source) == expected


def test_052():
    source = """
    func main() -> void {
        let i = 0;
        while (i < 5) {
            i = i + 1;
            if (i % 2 == 0) {continue;}
            print("" + i);
        }
    }
    """
    expected = "1\n3\n5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_053():
    source = """
    func main() -> void {
        for (i in [1, 2, 3, 4]) {
            if (i == 3) {break;}
            print("" + i);
        }
    }
    """
    expected = "1\n2"
    assert CodeGenerator().generate_and_run(source) == expected


def test_054():
    source = """
    func main() -> void {
        for (i in [1, 2, 3, 4]) {
            if (i % 2 == 0) {continue;}
            print("" + i);
        }
    }
    """
    expected = "1\n3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_55():
    source = """
    func checkPositive(n: int) -> string {
        if (n > 0) { return "positive"; }
        else { return "non-positive"; }
    }
    func main() -> void {
        print(checkPositive(5));
    }
    """
    expected = "positive"
    assert CodeGenerator().generate_and_run(source) == expected

def test_56():
    source = """
    func checkEvenOdd(n: int) -> string {
        if (n % 2 == 0) { return "even"; }
        else { return "odd"; }
    }
    func main() -> void {
        print(checkEvenOdd(4));
    }
    """
    expected = "even"
    assert CodeGenerator().generate_and_run(source) == expected



def test_057():
    source = """
    func main() -> void {
        let sum = 0;
        let i = 1;
        while (i <= 5) {
            sum = sum + i;
            i = i + 1;
        }
        print("" + sum);
    }
    """
    expected = "15"
    assert CodeGenerator().generate_and_run(source) == expected

def test_58():
    source = """
    func sign(n: int) -> string {
        if (n > 0) { return "positive"; }
        else if (n < 0) { return "negative"; }
        else { return "zero"; }
    }
    func main() -> void {
        print(sign(-3));
    }
    """
    expected = "negative"
    assert CodeGenerator().generate_and_run(source) == expected



def test_059():
    source = """
    func main() -> void {
        let result = "";
        for (i in [1, 2, 3]) {
            for (j in [4, 5]) {
                if (j == 5) {continue;}
                result = result + i + j;
            }
        }
        print(result);
    }
    """
    expected = "142434"
    assert CodeGenerator().generate_and_run(source) == expected


def test_60():
    source = """
    func grade(score: int) -> string {
        if (score >= 90) { return "A"; }
        else if (score >= 80) { return "B"; }
        else if (score >= 70) { return "C"; }
        else { return "F"; }
    }
    func main() -> void {
        print(grade(75));
    }
    """
    expected = "C"
    assert CodeGenerator().generate_and_run(source) == expected


def test_061():
    source = """
    func main() -> void {
        let i = 0;
        while (true) {
            if (i == 3) {break;}
            print("" + i);
            i = i + 1;
        }
    }
    """
    expected = "0\n1\n2"
    assert CodeGenerator().generate_and_run(source) == expected





def test_62():
    source = """
    func compare(a: int, b: int) -> string {
        if (a > b) { return "greater"; }
        else if (a < b) { return "less"; }
        else { return "equal"; }
    }
    func main() -> void {
        print(compare(5, 5));
    }
    """
    expected = "equal"
    assert CodeGenerator().generate_and_run(source) == expected




def test_063():
    source = """
    func main() -> void {
        for (x in [1, 2, 3, 4]) {
            if (x == 2) {continue;}
            if (x == 4) {break;}
            print("" + x);
        }
    }
    """
    expected = "1\n3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_64():
    source = """
    func truth(val: bool) -> int {
        if (val) { return 1; }
        else { return 0; }
    }
    func main() -> void {
        print("" + truth(true));
    }
    """
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected

def test_65():
    source = """
    func classifyNum(n: int) -> string {
        if (n < 0) { return "negative"; }
        else if (n == 0) { return "zero"; }
        else if (n < 10) { return "small"; }
        else { return "large"; }
    }
    func main() -> void {
        print(classifyNum(15));
    }
    """
    expected = "large"
    assert CodeGenerator().generate_and_run(source) == expected

def test_066():
    source = """
    func main() -> void {
        let i = 0;
        while (i < 10) {
            i = i + 1;
            if (i < 5) {continue;}
            if (i == 8) {break;}
            print("" + i);
        }
    }
    """
    expected = "5\n6\n7"
    assert CodeGenerator().generate_and_run(source) == expected

def test_67():
    source = """
    func isVowel(c: string) -> bool {
        if (c == "a") { return true; }
        else { return false; }
    }
    func main() -> void {
        print(bool2str(isVowel("b")));
    }
    """
    expected = "false"
    assert CodeGenerator().generate_and_run(source) == expected

def test_68():
    source = """
    func numberType(n: int) -> string {
        if (n < 0) { return "negative"; }
        else if (n == 0) { return "zero"; }
        else { return "positive"; }
    }
    func main() -> void {
        print(numberType(0));
    }
    """
    expected = "zero"
    assert CodeGenerator().generate_and_run(source) == expected

def test_69():
    source = """
    func absVal(n: int) -> int {
        if (n >= 0) { return n; }
        else { return -n; }
    }
    func main() -> void {
        print("" + absVal(-8));
    }
    """
    expected = "8"
    assert CodeGenerator().generate_and_run(source) == expected


def test_070():
    source = """
    func main() -> void {
        let counter = 0;
        for (n in [10, 20, 30]) {
            counter = counter + 1;
            if (n == 20) {continue;}
            print("" + n);
        }
        print("count=" + counter);
    }
    """
    expected = "10\n30\ncount=3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_071():
    source = """
    func main() -> void {
        let a = 5;
        let b = 2;
        print("" + (a % b));
    }
    """
    expected = "1"
    assert CodeGenerator().generate_and_run(source) == expected


def test_072():
    source = """
    func main() -> void {
        let s = "x";
        for (i in [1, 2, 3]) {
            s = s + i;
        }
        print(s);
    }
    """
    expected = "x123"
    assert CodeGenerator().generate_and_run(source) == expected


def test_073():
    source = """
    func fact(n: int) -> int {
        if (n <= 1) { return 1; }
        else { return n * fact(n - 1); }
    }
    func main() -> void {
        print("" + fact(5));
    }
    """
    expected = "120"
    assert CodeGenerator().generate_and_run(source) == expected


def test_074():
    source = """
    func main() -> void {
        let arr: [int; 4] = [2, 4, 6, 8];
        let sum = 0;
        for (x in arr) { sum = sum + x; }
        print("" + sum);
    }
    """
    expected = "20"
    assert CodeGenerator().generate_and_run(source) == expected


def test_075():
    source = """
    func main() -> void {
        if (true || false) { print("yes"); }
        else { print("no"); }
    }
    """
    expected = "yes"
    assert CodeGenerator().generate_and_run(source) == expected


def test_076():
    source = """
    func greet(name: string) -> string {
        return "Hello, " + name;
    }
    func main() -> void {
        print(greet("world"));
    }
    """
    expected = "Hello, world"
    assert CodeGenerator().generate_and_run(source) == expected


def test_077():
    source = """
    func main() -> void {
        let a = [true, false, true];
        print("" + a[0]);
        print("" + a[1]);
        print("" + a[2]);
    }
    """
    expected = "true\nfalse\ntrue"
    assert CodeGenerator().generate_and_run(source) == expected


def test_078():
    source = """
    func main() -> void {
        let x = 2.5;
        let y = 4;
        print("" + (x * y));
    }
    """
    expected = "10.0"
    assert CodeGenerator().generate_and_run(source) == expected


def test_079():
    source = """
    func main() -> void {
        let text = "";
        let i = 1;
        while (i <= 3) {
            text = text + i;
            i = i + 1;
        }
        print(text);
    }
    """
    expected = "123"
    assert CodeGenerator().generate_and_run(source) == expected


def test_080():
    source = """
    func sum(a:int) -> int {
        return a + a + a;
    }
    func main() -> void {
        print("" + sum(10));
    }
    """
    expected = "30"
    assert CodeGenerator().generate_and_run(source) == expected
def test_081():
    source = """
    func main() -> void {
        for (i in [1, 2, 3, 4, 5]) {
            if (i > 3) {break;}
            print("" + i);
        }
    }
    """
    expected = "1\n2\n3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_082():
    source = """
    func main() -> void {
        let i = 0;
        while (i < 6) {
            i = i + 1;
            if (i % 2 == 0) {continue;}
            print("" + i);
        }
    }
    """
    expected = "1\n3\n5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_083():
    source = """
    func main() -> void {
        let count = 0;
        for (x in [1, 2, 3]) {
            for (y in [10, 20]) {
                if (y == 20) {break;}
                print("" + x + y);
                count = count + 1;
            }
        }
        print("count=" + count);
    }
    """
    expected = "110\n210\n310\ncount=3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_084():
    source = """
    func main() -> void {
        for (n in [1, 2, 3, 4]) {
            if (n < 3) {continue;}
            print("" + n);
        }
    }
    """
    expected = "3\n4"
    assert CodeGenerator().generate_and_run(source) == expected


def test_085():
    source = """
    func main() -> void {
        let sum = 0;
        let i = 0;
        while (true) {
            i = i + 1;
            if (i == 4) {break;}
            sum = sum + i;
        }
        print("" + sum);
    }
    """
    expected = "6"
    assert CodeGenerator().generate_and_run(source) == expected


def test_086():
    source = """
    func main() -> void {
        let out = "";
        for (i in [1, 2, 3]) {
            for (j in [1, 2, 3]) {
                if (i == j) {continue;}
                out = out + i + j;
            }
        }
        print(out);
    }
    """
    expected = "121321233132"
    assert CodeGenerator().generate_and_run(source) == expected


def test_087():
    source = """
    func main() -> void {
        let i = 0;
        while (i < 5) {
            if (i == 2) {
                i = i + 1;
                continue;
            }
            print("" + i);
            i = i + 1;
        }
    }
    """
    expected = "0\n1\n3\n4"
    assert CodeGenerator().generate_and_run(source) == expected


def test_088():
    source = """
    func main() -> void {
        for (x in [5, 4, 3, 2, 1]) {
            if (x % 2 == 0) {continue;}
            if (x == 1) {break;}
            print("" + x);
        }
    }
    """
    expected = "5\n3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_089():
    source = """
    func main() -> void {
        let result = "";
        for (a in [1, 2]) {
            for (b in [3, 4]) {
                if (a + b == 5) {continue;}
                result = result + a + b;
            }
        }
        print(result);
    }
    """
    expected = "1324"
    assert CodeGenerator().generate_and_run(source) == expected


def test_090():
    source = """
    func main() -> void {
        let i = 0;
        while (true) {
            if (i == 2) {i = i + 1; continue;}
            if (i >= 4) {break;}
            print("" + i);
            i = i + 1;
        }
    }
    """
    expected = "0\n1\n3"
    assert CodeGenerator().generate_and_run(source) == expected

def test_091():
    source = """
    func loopAndBreak() -> int {
        for (i in [1, 2, 3, 4]) {
            if (i == 3) {break;}
            print("" + i);
        }
        return 42;
    }
    func main() -> void {
        let x = loopAndBreak();
        print("" + x);
    }
    """
    expected = "1\n2\n42"
    assert CodeGenerator().generate_and_run(source) == expected


def test_092():
    source = """
    func skipEvenPrintOdd(limit: int) -> void {
        let i = 0;
        while (i <= limit) {
            i = i + 1;
            if (i % 2 == 0) {continue;}
            print("" + i);
        }
    }
    func main() -> void {
        skipEvenPrintOdd(5);
    }
    """
    expected = "1\n3\n5"
    assert CodeGenerator().generate_and_run(source) == expected


def test_093():
    source = """
    func firstMultipleOfThree() -> int {
        for (n in [2,3,5,9,10,12]) {
            if (n % 3 == 0) {return n;}
        }
        return -1;
    }
    func main() -> void {
        print("" + firstMultipleOfThree());
    }
    """
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_094():
    source = """
    func findBeforeFive() -> void {
        for (n in [1,2,3,5,6]) {
            if (n == 5) {break;}
            print("" + n);
        }
    }
    func main() -> void {
        findBeforeFive();
    }
    """
    expected = "1\n2\n3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_095():
    source = """
    func main() -> void {
        for (i in [1, 2, 3]) {
            for (j in [1, 2, 3]) {
                if (i * j > 4) {break;}
                print("" + i + j);
            }
        }
    }
    """
    expected = "11\n12\n13\n21\n22\n31"
    assert CodeGenerator().generate_and_run(source) == expected


def test_096():
    source = """
    func loopWithReturn() -> string {
        for (c in ["a", "b", "stop", "c"]) {
            if (c == "stop") {return "done";}
        }
        return "not found";
    }
    func main() -> void {
        print(loopWithReturn());
    }
    """
    expected = "done"
    assert CodeGenerator().generate_and_run(source) == expected


def test_097():
    source = """
    func main() -> void {
        let count = 0;
        while (true) {
            count = count + 1;
            if (count < 3) {continue;}
            break;
        }
        print("" + count);
    }
    """
    expected = "3"
    assert CodeGenerator().generate_and_run(source) == expected


def test_098():
    source = """
    func innerLoopBreak() -> void {
        for (x in [1, 2]) {
            for (y in [1, 2, 3]) {
                if (y == 2) {break;}
                print("" + x + y);
            }
        }
    }
    func main() -> void {
        innerLoopBreak();
    }
    """
    expected = "11\n21"
    assert CodeGenerator().generate_and_run(source) == expected


def test_099():
    source = """
    func skipUntilThree() -> void {
        let nums = [1, 2, 3, 4];
        for (n in nums) {
            if (n < 3) {continue;}
            print("" + n);
        }
    }
    func main() -> void {
        skipUntilThree();
    }
    """
    expected = "3\n4"
    assert CodeGenerator().generate_and_run(source) == expected


def test_100():
    source = """
    func main() -> void {
        let out = "";
        for (a in [1, 2]) {
            for (b in [1, 2]) {
                if (a + b == 3) {continue;}
                out = out + a + b;
            }
        }
        print(out);
    }
    """
    expected = "1122"
    assert CodeGenerator().generate_and_run(source) == expected
