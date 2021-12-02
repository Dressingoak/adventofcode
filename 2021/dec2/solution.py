import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def compute(file: str):
    horizontal = 0
    vertical = 0
    f = open(file, "r")
    for line in f.readlines():
        match line.strip().split():
            case ["forward", x]:
                horizontal += int(x)
            case ["down", x]:
                vertical += int(x)
            case ["up", x]:
                vertical -= int(x)
    return horizontal * vertical

print("Dec 2, part 1: {}".format(compute(file)))
