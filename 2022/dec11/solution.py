import sys
import re

def combine(a, b):
    d = {k: v for k, v in a.items()}
    for k, v in b.items():
        if k in d:
            d[k] += v
        else:
            d[k] = v
    return d

def increment(a, kk):
    d = {k: v for k, v in a.items()}
    if kk not in d:
        d[kk] = 0
    d[kk] += 1
    return d

class Monkey:
    relief = None

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
            new //= self.relief
            if new % self.test == 0:
                monkeys[self.true].catch(new)
            else:
                monkeys[self.false].catch(new)
        self.items = []

    def catch(self, item):
        self.items.append(item)

    def throw2(self, monkeys, id, value, turns, known = {}):
        # print(id, value, turns)
        if turns == 0:
            return known
        next_value = self.op(value)
        next_known = increment(known, id)
        next_id = self.true if next_value % self.test == 0 else self.false
        next_turn = turns if next_id > id else turns - 1
        return monkeys[next_id].throw2(monkeys, next_id, next_value, next_turn, next_known)

def parse_op(op, rhs, mod=None):
    match (op, rhs):
        case ("*", v) if v == "old": return lambda x: x**2 if mod is None else (x % mod)**2
        case ("*", v): return lambda x: x * int(v) if mod is None else (x % mod) * (int(v) % mod)
        case ("+", v): return lambda x: x + int(v) if mod is None else (x % mod) + (int(v) % mod)
        case _: raise Exception(f"Could not parse \"new = old {op} {rhs}\"")

def parse(file: str, mod=False):
    pattern = re.compile(r"Monkey (?P<id>\d):\s+Starting items: (?P<items>[\d, ]+\d)+\s+Operation: new = old (?P<op>\+|\*) (?P<rhs>old|\d+)\s+Test: divisible by (?P<test>\d+)\s+If true: throw to monkey (?P<true>\d)\s+If false: throw to monkey (?P<false>\d)")
    with open(file, "r") as f:
        s = f.read()
    expected = s.count("\n") // 7 + 1
    monkeys = []
    for m in re.finditer(pattern, s):
        d = m.groupdict()
        items = [int(_) for _ in d["items"].split(", ")]
        test = int(d["test"])
        op = parse_op(d["op"], d["rhs"], test if mod else None)
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
    Monkey.relief = 3
    monkeys = parse(file)
    for _ in range(20):
        for i in range(len(monkeys)):
            monkeys[i].throw(monkeys)
    inspections = [monkey.inspections for monkey in monkeys]
    inspections.sort(reverse=True)
    match inspections:
        case [a, b, *_]: return a * b

def calculate_part2(file: str):
    Monkey.relief = 1
    monkeys = parse(file)
    for _ in range(2):
        for i in range(len(monkeys)):
            monkeys[i].throw(monkeys)
    for i, monkey in enumerate(monkeys):
        print(f"Monkey {i}: {monkey.inspections}")
    inspections = [monkey.inspections for monkey in monkeys]
    inspections.sort(reverse=True)
    match inspections:
        case [a, b, *_]: return a * b

def calculate_part2b(file: str):
    Monkey.relief = 1
    monkeys = parse(file)
    d = {}
    for id, monkey in enumerate(monkeys):
        for item in monkey.items:
            # print(id, item)
            # itemz = monkey.op(item % monkey.test) % monkey.test
            d = combine(d, monkey.throw2(monkeys, id, item, 700))
    monkey_inspections = sorted((k, v) for k, v in d.items())
    for i, inspections in monkey_inspections:
        print(f"Monkey {i}: {inspections}")
    inspections = [inspections for (_, inspections) in monkey_inspections]
    inspections.sort(reverse=True)
    match inspections:
        case [a, b, *_]: return a * b
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 11, part 1: {}".format(calculate_part1(file)))

    print("Dec 11, part 2: {}".format(calculate_part2(file)))
    print("Dec 11, part 2b: {}".format(calculate_part2b(file)))
