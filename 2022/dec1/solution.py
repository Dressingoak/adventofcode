import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def calculate(file: str):
    cur, max = 0, 0
    f = open(file, "r")
    for line in f.readlines():
        match line.strip():
            case "":
                if cur > max:
                    max = cur
                cur = 0
            case x:
                cur += int(x)
    return max

print("Dec 1, part 1: {}".format(calculate(file)))
