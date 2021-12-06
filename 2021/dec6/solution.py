import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[int]:
    f = open(file, "r")
    return [int(_) for _ in f.readline().strip().split(",")]

def advance(timer: int, n: int) -> int:
    if n <= timer:
        return 1
    elif timer > 0:
        return advance(0, n - timer)
    elif timer == 0:
        return advance(6, n - 1) + advance(8, n - 1)

def compute(data: list[int], n: int):
    return sum(advance(s, n) for s in data)

data = read(file)

print("Dec 6, part 1: {}".format(compute(data, 80)))
