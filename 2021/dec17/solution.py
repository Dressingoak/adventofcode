import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str) -> tuple[tuple[int, int], tuple[int, int]]:
    r = re.compile('target area: x=(-*\d+)\.\.(-*\d+), y=(-*\d+)\.\.(-*\d+)')
    f = open(file, "r")
    m = r.match(f.readline().strip())
    x1, x2, y1, y2 = tuple(map(lambda x: int(x), list(m.group(1, 2, 3, 4))))
    return (x1, x2), (y1, y2)

def triangular(n: int):
    return n * (n + 1) // 2

def triangular_inv(x: int):
    l = x // 2
    for n in range(l - 1, -1, -1):
        if triangular(n) < x:
            return l
        else:
            l -= 1

def max_y(data: tuple[tuple[int, int], tuple[int, int]]):
    _, (y_low, _) = data
    v = (0 - y_low) - 1
    return triangular(v)

def simulate(data: tuple[tuple[int, int], tuple[int, int]]):
    (x1, x2), (y1, y2) = data
    vx1, vx2 = triangular_inv(x1), x2
    vy1, vy2 = y1, -y1
    c = 0
    for vxi in range(vx1, vx2 + 1):
        for vyi in range(vy1, vy2 + 1):
            x, y = 0, 0
            vx, vy = vxi, vyi
            while x <= x2 and y >= y1:
                x += vx
                if vx > 0:
                    vx -= 1
                y += vy
                vy -= 1
                if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                    c += 1
                    break
    return c

data = read(file)

print("Dec 17, part 1: {}".format(max_y(data)))
print("Dec 17, part 2: {}".format(simulate(data)))
