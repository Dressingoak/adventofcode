import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> list[bool]:
    r = re.compile('target area: x=(-*\d+)\.\.(-*\d+), y=(-*\d+)\.\.(-*\d+)')
    f = open(file, "r")
    m = r.match(f.readline().strip())
    x1, x2, y1, y2 = tuple(map(lambda x: int(x), list(m.group(1, 2, 3, 4))))
    return (x1, x2), (y1, y2)

def max_y(data: tuple[tuple[int, int], tuple[int, int]]):
    _, (y_low, _) = data
    v = (0 - y_low) - 1
    return v * (v + 1) // 2

data = read(file)

print("Dec 17, part 1: {}".format(max_y(data)))
