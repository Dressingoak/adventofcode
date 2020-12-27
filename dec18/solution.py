import re

exprs = open("input.txt").read().strip().split("\n")

def calculate(expr):
    pattern = re.compile(r'([\*\+])\s*(\d+)')
    m1 = re.match(r'^(\d+)', expr)
    if m1:
        value = int(m1.group(1))
        for m2 in re.finditer(pattern, expr):
            operation = m2.group(1)
            operand = int(m2.group(2))
            if operation == "*":
                value *= operand
            elif operation == "+":
                value += operand
            else:
                raise Exception("Operation '{}' not supported".format(operation))
        return value
    else:
        raise Exception("Cannot evaluate expression, got '{}'".format(expr))

def evaluate(expr):
    pattern = re.compile(r'\(([\*\+\d\s]+)\)')
    left = 0
    s = ""
    matched = False
    for m in re.finditer(pattern, expr):
        matched = True
        l = m.start()
        r = m.end()
        s += expr[left:l]
        s += str(calculate(m.group(1)))
        left = r
    s += expr[left:]
    if matched:
        return evaluate(s)
    else:
        return calculate(s)

print("Part 1: {}".format(sum(evaluate(_) for _ in exprs)))
