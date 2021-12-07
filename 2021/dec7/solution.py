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

data = read(file)

print("Dec 6, part 1: {}".format(compute(data)))
