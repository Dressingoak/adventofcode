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
        if p1.x == p2.x:
            lower = min(p1.y, p2.y)
            upper = max(p1.y, p2.y)
            self.dir = 3 # South
            self.p = Point(p1.x, lower)
            self.size = upper - lower + 1
        elif p1.y == p2.y:
            left = min(p1.x, p2.x)
            right = max(p1.x, p2.x)
            self.dir = 1 # East
            self.p = Point(left, p1.y)
            self.size = right - left + 1
        elif p1.x < p2.x and p1.y < p2.y:
            self.dir = 2 # South-east
            self.p = Point(p1.x, p1.y)
            self.size = p2.x - p1.x + 1
        elif p1.x > p2.x and p1.y > p2.y:
            self.dir = 2 # South-east
            self.p = Point(p2.x, p2.y)
            self.size = p1.x - p2.x + 1
        elif p1.x < p2.x and p1.y > p2.y:
            self.dir = 0 # North-east
            self.p = Point(p1.x, p1.y)
            self.size = p2.x - p1.x + 1
        elif p1.x > p2.x and p1.y < p2.y:
            self.dir = 0 # North-east
            self.p = Point(p2.x, p2.y)
            self.size = p1.x - p2.x + 1
        else:
            raise Exception("Unhandled case.")
    
    def draw(self):
        match self.dir:
            case 0: return {Point(self.p.x + t, self.p.y - t) for t in range(self.size)}
            case 1: return {Point(self.p.x + t, self.p.y) for t in range(self.size)}
            case 2: return {Point(self.p.x + t, self.p.y + t) for t in range(self.size)}
            case 3: return {Point(self.p.x, self.p.y + t) for t in range(self.size)}

    def __str__(self) -> str:
        return "d: {}, p: {}, size: {}".format(self.dir, self.p, self.size)

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
    floor = dict()
    for s in data:
        for p in s.draw():
            if p in floor:
                floor[p] += 1
            else:
                floor[p] = 1
    return sum(1 for (p, v) in floor.items() if v > 1)

data = read(file)
filtered = [s for s in data if s.dir == 1 or s.dir == 3]

print("Dec 5, part 1: {}".format(compute(filtered)))
print("Dec 5, part 2: {}".format(compute(data)))
