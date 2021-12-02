import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def compute(file: str):
    horizontal = 0
    depth = 0
    f = open(file, "r")
    for line in f.readlines():
        match line.strip().split():
            case ["forward", x]:
                horizontal += int(x)
            case ["down", x]:
                depth += int(x)
            case ["up", x]:
                depth -= int(x)
    return horizontal * depth

def compute_with_aim(file: str):
    horizontal = 0
    depth = 0
    aim = 0
    f = open(file, "r")
    for line in f.readlines():
        match line.strip().split():
            case ["forward", x]:
                horizontal += int(x)
                depth += aim * int(x)
            case ["down", x]:
                aim += int(x)
            case ["up", x]:
                aim -= int(x)
    return horizontal * depth

print("Dec 2, part 1: {}".format(compute(file)))
print("Dec 2, part 2: {}".format(compute_with_aim(file)))
