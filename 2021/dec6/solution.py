import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[int]:
    f = open(file, "r")
    return [int(_) for _ in f.readline().strip().split(",")]

known = dict()

def advance(timer: int, n: int) -> int:
    if (n, timer) in known:
        return known[(n, timer)]
    if n <= timer:
        r = 1
    elif timer > 0:
        r = advance(0, n - timer)
    else:
        r = advance(6, n - 1) + advance(8, n - 1)
    known[(n, timer)] = r
    return r

def compute(data: list[int], n: int):
    return sum(advance(s, n) for s in data)

data = read(file)

print("Dec 6, part 1: {}".format(compute(data, 80)))
print("Dec 6, part 2: {}".format(compute(data, 256)))
