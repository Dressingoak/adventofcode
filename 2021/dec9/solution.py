import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[list[int]]:
    f = open(file, "r")
    return [[int(_) for _ in line.strip()] for line in f.readlines()]

def find_low_points(data):
    rows = len(data)
    cols = len(data[0])
    for i in range(rows):
        for j in range(cols):
            value = data[i][j]
            adjacent_x = [data[k][j] for k in [i - 1, i + 1] if k in range(rows)]
            adjacent_y = [data[i][l] for l in [j - 1, j + 1] if l in range(cols)]
            if all(value < adj for adj in adjacent_x + adjacent_y):
                yield value

def calculate_risk_value_sum(data):
    return sum(r + 1 for r in find_low_points(data))

data = read(file)

print("Dec 9, part 1: {}".format(calculate_risk_value_sum(data)))
