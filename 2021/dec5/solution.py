import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)

class LineSegment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def box(self):
        if self.p1.x == self.p2.x:
            lower = min(self.p1.y, self.p2.y)
            upper = max(self.p1.y, self.p2.y)
            return (0, self.p1.x, lower, upper)
        elif self.p1.y == self.p2.y:
            left = min(self.p1.x, self.p2.x)
            right = max(self.p1.x, self.p2.x)
            return (1, self.p1.y, left, right)
        else:
            raise Exception("Can only handle vertical or horizontal line segments.")

    def get_points(self):
        if self.p1.x == self.p2.x:
            lower = min(self.p1.y, self.p2.y)
            upper = max(self.p1.y, self.p2.y)
            return set(Point(self.p1.x, y) for y in range(lower, upper + 1))
        elif self.p1.y == self.p2.y:
            left = min(self.p1.x, self.p2.x)
            right = max(self.p1.x, self.p2.x)
            return set(Point(x, self.p1.y) for x in range(left, right + 1))
        else:
            raise Exception("Can only handle vertical or horizontal line segments.")

    def overlap(self, other):
        p1 = self.get_points()
        p2 = other.get_points()
        return p1.intersection(p2)

    def __str__(self) -> str:
        return "{} -> {}".format(self.p1, self.p2)

def read(file: str) -> list[LineSegment]:
    f = open(file, "r")
    p = re.compile('(\d+),(\d+)\s+->\s+(\d+),(\d+)')
    segments = []
    for line in f.readlines():
        m = p.match(line)
        coords = tuple(int(_) for _ in m.group(1, 2, 3, 4))
        segments.append(LineSegment(Point(coords[0], coords[1]), Point(coords[2], coords[3])))
    return segments

def compute(data: list[LineSegment]):
    c = set()
    filtered = [s for s in data if s.p1.x == s.p2.x or s.p1.y == s.p2.y]
    n = len(filtered)
    for i in range(n):
        for j in range(i+1,n):
            c.update(filtered[i].overlap(filtered[j]))
    return len(c)

data = read(file)

print("Dec 5, part 1: {}".format(compute(data)))
