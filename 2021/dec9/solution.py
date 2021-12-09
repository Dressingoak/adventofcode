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
            adjacent_x = [(k, j) for k in [i - 1, i + 1] if k in range(rows)]
            adjacent_y = [(i, l) for l in [j - 1, j + 1] if l in range(cols)]
            if all(value < data[k][l] for (k, l) in adjacent_x + adjacent_y):
                yield (i, j)

def calculate_risk_value_sum(data):
    return sum(data[i][j] + 1 for (i, j) in find_low_points(data))

visited = set()

def count_basin(data, i, j, rows, cols):
    if (i, j) in visited:
        return 0
    visited.add((i, j))
    adjacent_x = [(k, j) for k in [i - 1, i + 1] if k in range(rows) and (k, j) not in visited]
    adjacent_y = [(i, l) for l in [j - 1, j + 1] if l in range(cols) and (i, l) not in visited]
    adjacent = [(k, l) for (k, l) in adjacent_x + adjacent_y if data[k][l] < 9]
    return 1 + sum(count_basin(data, k, l, rows, cols) for (k, l) in adjacent)

def count_basins(data):
    rows = len(data)
    cols = len(data[0])
    sizes = []
    for (i, j) in find_low_points(data):
        sizes.append(count_basin(data, i, j, rows, cols))
    sizes.sort(reverse = True)
    return sizes[0] * sizes[1] * sizes[2]

data = read(file)

print("Dec 9, part 1: {}".format(calculate_risk_value_sum(data)))
print("Dec 9, part 2: {}".format(count_basins(data)))
