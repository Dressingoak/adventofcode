import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[int]:
    f = open(file, "r")
    return [int(_) for _ in f.readline().strip().split(",")]

def compute(data: list[int]):
    least = min(data)
    greatest = max(data)
    tries = []
    for i in range(least, greatest + 1):
        tries.append(sum(abs(j - i) for j in data))
    return min(tries)

def compute_with_growing_cost(data: list[int]):
    least = min(data)
    greatest = max(data)
    data.sort()
    tries = []
    for i in range(least, greatest + 1):
        s = 0
        for j in data:
            d = abs(j - i)
            s += d * (d + 1) // 2
        tries.append(s)
    return min(tries)

data = read(file)

print("Dec 6, part 1: {}".format(compute(data)))
print("Dec 6, part 2: {}".format(compute_with_growing_cost(data)))
