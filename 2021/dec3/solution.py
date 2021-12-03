import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str):
    f = open(file, "r")
    return [list(int(_) for _ in line.strip()) for line in f.readlines()]

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

def compute_life_support_subrating(crit: bool, data: list[list[int]], j: int = 0):
    rows = len(data)
    cols = len(data[0])
    if rows == 1:
        number = data[0]
        return sum(number[i] * 2**(cols - i - 1) for i in range(cols))
    elif j < cols and rows > 1:
        ones = sum(data[i][j] for i in range(rows))
        zeros = rows - ones
        bit = int(ones >= zeros if crit else ones < zeros)
        new_data = list(filter(lambda row: row[j] == bit, data))
        return compute_life_support_subrating(crit, new_data, j + 1)
    else:
        raise Exception("Error")

def compute_life_support_rating(data: list[list[int]]):
    return compute_life_support_subrating(True, data) * compute_life_support_subrating(False, data)


print("Dec 3, part 1: {}".format(compute(read(file))))
print("Dec 3, part 2: {}".format(compute_life_support_rating(read(file))))
