import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str):
    f = open(file, "r")
    return [int(line.strip()) for line in f.readlines()]

def compute(data: list[int]):
    increases = 0
    prev = None
    for x in data:
        if prev is None:
            prev = x
            continue
        if x > prev:
            increases += 1
        prev = x
    return increases

def compute_with_window(data: list[int]):
    size = 3
    windows = [sum(map(lambda j: data[j], range(i,i+size))) for i in range(0,len(data)-size+1)]
    return compute(windows)

data = read(file)
print("Dec 1, part 1: {}".format(compute(data)))
print("Dec 1, part 2: {}".format(compute_with_window(data)))
