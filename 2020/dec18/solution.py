import re
from math import prod

exprs = open("input.txt").read().strip().split("\n")

def calculate_wo_precedence(expr):
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

def calculate_with_precedence(expr):
    pattern = re.compile(r'(\d+)\s*\+\s*(\d+)')
    left = 0
    s = ""
    matched = False
    for m in re.finditer(pattern, expr):
        matched = True
        l = m.start()
        r = m.end()
        first = int(m.group(1))
        second = int(m.group(2))
        s += expr[left:l]
        s += str(first + second)
        left = r
    s += expr[left:]
    if matched:
        return calculate_with_precedence(s)
    else:
        dpattern = re.compile(r'(\d+)')
        value = prod([int(_) for _ in re.findall(dpattern, s)])
        return value

def evaluate(expr, method):
    pattern = re.compile(r'\(([\*\+\d\s]+)\)')
    left = 0
    s = ""
    matched = False
    for m in re.finditer(pattern, expr):
        matched = True
        l = m.start()
        r = m.end()
        s += expr[left:l]
        s += str(method(m.group(1)))
        left = r
    s += expr[left:]
    if matched:
        return evaluate(s, method)
    else:
        return method(s)

print("Part 1: {}".format(sum(evaluate(_, calculate_wo_precedence) for _ in exprs)))

print("Part 2: {}".format(sum(evaluate(_, calculate_with_precedence) for _ in exprs)))
