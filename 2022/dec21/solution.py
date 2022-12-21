import sys
import re

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

def calculate_part1(file: str):
    monkeys = parse(file)
    return lookup("root", monkeys)

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 21, part 1: {}".format(calculate_part1(file)))
    # print("Dec 21, part 2: {}".format(calculate_part2(file)))
