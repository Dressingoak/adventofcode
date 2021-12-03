import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str):
    f = open(file, "r")
    return [list(int(_) for _ in line.strip()) for line in f.readlines()]

print(read(file))

def compute(data: list[list[int]]):
    rows = len(data)
    cols = len(data[0])
    gamma = 0
    epsilon = 0
    for j in range(cols):
        ones = sum(data[i][j] for i in range(rows))
        value = 2**(cols - j - 1)
        if ones > rows / 2:
            gamma += value
        else:
            epsilon += value
    return gamma * epsilon

print("Dec 3, part 1: {}".format(compute(read(file))))
