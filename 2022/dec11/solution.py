import sys
import re

class Monkey:
    def __init__(self, items, op, test, true, false):
        self.items = items
        self.op = op
        self.test = test
        self.true = true
        self.false = false
        self.inspections = 0

    def throw(self, monkeys):
        self.inspections += len(self.items)
        for item in self.items:
            new = self.op(item)
            new //= 3
            if new % self.test == 0:
                monkeys[self.true].catch(new)
            else:
                monkeys[self.false].catch(new)
        self.items = []

    def catch(self, item):
        self.items.append(item)

def parse_op(op, rhs):
    match (op, rhs):
        case ("*", v) if v == "old": return lambda x: x**2
        case ("*", v): return lambda x: x * int(v)
        case ("+", v): return lambda x: x + int(v)
        case _: raise Exception(f"Could not parse \"new = old {op} {rhs}\"")

def parse(file: str):
    pattern = re.compile(r"Monkey (?P<id>\d):\s+Starting items: (?P<items>[\d, ]+\d)+\s+Operation: new = old (?P<op>\+|\*) (?P<rhs>old|\d+)\s+Test: divisible by (?P<test>\d+)\s+If true: throw to monkey (?P<true>\d)\s+If false: throw to monkey (?P<false>\d)")
    with open(file, "r") as f:
        s = f.read()
    expected = s.count("\n") // 7 + 1
    monkeys = []
    for m in re.finditer(pattern, s):
        d = m.groupdict()
        items = [int(_) for _ in d["items"].split(", ")]
        op = parse_op(d["op"], d["rhs"])
        test = int(d["test"])
        true = int(d["true"])
        false = int(d["false"])
        if int(d["id"]) == len(monkeys):
            monkeys.append(Monkey(items, op, test, true, false))
        else:
            raise Exception("Skipped an input...")
    if not expected == len(monkeys):
        raise Exception(f"Didn't parse entire input, expected {expected} blocks, got {len(monkeys)}.")
    return monkeys

def calculate_part1(file: str):
    monkeys = parse(file)
    for _ in range(20):
        for i in range(len(monkeys)):
            monkeys[i].throw(monkeys)
    inspections = [monkey.inspections for monkey in monkeys]
    inspections.sort(reverse=True)
    match inspections:
        case [a, b, *_]: return a * b

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 11, part 1: {}".format(calculate_part1(file)))
    # print("Dec 11, part 2: {}".format(calculate_part2(file)))
