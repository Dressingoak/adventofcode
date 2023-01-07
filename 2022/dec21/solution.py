import sys
import re
sys.path.append('../')
from timing import print_timing

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

class Fraction:
    def __init__(self, n: int, d: int) -> None:
        g = gcd(n, d)
        self.n, self.d = n // g, d // g
    
    def __repr__(self) -> str:
        return f"{self.n}/{self.d}" if self.d != 1 else f"{self.n}"

    def zero():
        return Fraction(0, 1)

    def __int__(self) -> int:
        if self.d != 1:
            raise RuntimeError(f"Error casting {self} to int, denominator is not zero!")
        return self.n

    def __neg__(self):
        return Fraction(-self.n, self.d)
    
    def __add__(self, other):
        if isinstance(other, Fraction):
            n = self.n * other.d + other.n * self.d
            d = self.d * other.d
            g = gcd(n, d)
            return Fraction(n // g, d // g)
        elif isinstance(other, int):
            return self + Fraction(other, 1)
        else:
            raise NotImplementedError()

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Fraction):
            n = self.n * other.n
            d = self.d * other.d
            g = gcd(n, d)
            return Fraction(n // g, d // g)
        elif isinstance(other, int):
            return self * Fraction(other, 1)
        else:
            raise NotImplementedError()

    def __truediv__(self, other):
        if isinstance(other, Fraction):
            if other.n == 0:
                raise ZeroDivisionError()
            else:
                n = self.n * other.d
                d = self.d * other.n
                g = gcd(n, d)
                return Fraction(n // g, d // g)
        elif isinstance(other, int):
            return self / Fraction(other, 1)
        else:
            raise NotImplementedError()

class Polynomial:
    def __init__(self, coef):
        self.coef = [Fraction(c, 1) if isinstance(c, int) else c for c in coef]
        self.n = len(self.coef) - 1

    def __repr__(self) -> str:
        return self.coef.__repr__()

    def __neg__(self):
        return Polynomial([-c for c in self.coef])
    
    def __add__(self, other):
        if isinstance(other, Polynomial):
            coef_lhs = [c for c in self.coef]
            coef_lhs.extend([Fraction.zero(),] * max(other.n - self.n, 0))
            coef_rhs = [c for c in other.coef]
            coef_rhs.extend([Fraction.zero(),] * max(self.n - other.n, 0))
            coef = [a + b for a, b in zip(coef_lhs, coef_rhs)]
        elif isinstance(other, Fraction):
            coef = [c for c in self.coef]
            coef[0] += other
        else:
            raise NotImplementedError(f"Cannot add Polynomial and {type(other)}")
        return Polynomial(coef)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            poly = Polynomial([0])
            for i, c in enumerate(self.coef):
                poly = poly + Polynomial([0,] * i + [c * cc for cc in other.coef])
            return poly
        elif isinstance(other, Fraction):
            coef = [c * other for c in self.coef]
        else:
            raise NotImplementedError(f"Cannot multiply Polynomial and {type(other)}")
        return Polynomial(coef)

    def __truediv__(self, other):
        if isinstance(other, Polynomial) and other.n == 0:
            coef = [c / other.coef[0] for c in self.coef]
        elif isinstance(other, Fraction):
            coef = [c / other for c in self.coef]
        else:
            raise NotImplementedError(f"Cannot divide Polynomial and {type(other)}")
        return Polynomial(coef)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__div__(self, other)

def parse(file: str):
    monkeys = {}
    pattern = re.compile(r"(\w{4}): ((\d+)|(\w{4}) ([\-\+\*\/]) (\w{4}))")
    with open(file, "r") as f:
        for line in f.readlines():
            match re.match(pattern, line).groups():
                case (name, _, number, None, None, None):
                    monkeys[name] = int(number)
                case (name, _, None, lhs, op, rhs):
                    monkeys[name] = (lhs, rhs, op)
                case _: raise Exception("Unhandled")
    return monkeys

def lookup(key: str, monkeys: dict[str, int | tuple[str, str, str]]):
    match monkeys[key]:
        case x if isinstance(x, int): return x
        case (lhs, rhs, op) if op == "+": return lookup(lhs, monkeys) + lookup(rhs, monkeys)
        case (lhs, rhs, op) if op == "-": return lookup(lhs, monkeys) - lookup(rhs, monkeys)
        case (lhs, rhs, op) if op == "*": return lookup(lhs, monkeys) * lookup(rhs, monkeys)
        case (lhs, rhs, op) if op == "/": return lookup(lhs, monkeys) // lookup(rhs, monkeys)
        case _: raise Exception("Unhandled")

def lookup_poly(key: str, monkeys: dict[str, int | tuple[str, str, str]], indent = 0):
    match (key, monkeys[key]):
        case ("humn", _): return Polynomial([0, 1])
        case (_, x) if isinstance(x, int): return Polynomial([x])
        case ("root", (lhs, rhs, _)): return lookup_poly(lhs, monkeys, indent + 2) - lookup_poly(rhs, monkeys, indent + 2)
        case (_, (lhs, rhs, op)) if op == "+": return lookup_poly(lhs, monkeys, indent + 2) + lookup_poly(rhs, monkeys, indent + 2)
        case (_, (lhs, rhs, op)) if op == "-": return lookup_poly(lhs, monkeys, indent + 2) - lookup_poly(rhs, monkeys, indent + 2)
        case (_, (lhs, rhs, op)) if op == "*": return lookup_poly(lhs, monkeys, indent + 2) * lookup_poly(rhs, monkeys, indent + 2)
        case (_, (lhs, rhs, op)) if op == "/": return lookup_poly(lhs, monkeys, indent + 2) / lookup_poly(rhs, monkeys, indent + 2)
        case _: raise Exception("Unhandled")

@print_timing
def calculate_part1(file: str):
    monkeys = parse(file)
    return lookup("root", monkeys)

@print_timing
def calculate_part2(file: str):
    monkeys = parse(file)
    equation = lookup_poly("root", monkeys)
    match equation.coef:
        case [b, a]: # Linear equation a * x + b = 0
            return int(-b / a)
        case coef:
            raise Exception(f"Unhandled, cannot solve equation og degree {len(coef) - 1}")
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 21, part 1: {} (took {})".format(*calculate_part1(file)))
    print("Dec 21, part 2: {} (took {})".format(*calculate_part2(file)))
