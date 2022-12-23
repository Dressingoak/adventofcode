import sys
import re

def parse(file: str):
    pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    with open(file, "r") as f:
        for line in f.readlines():
            m = re.match(pattern, line.strip())
            sx, sy, bx, by = [int(_) for _ in m.group(1, 2, 3, 4)]
            yield sx, sy, bx, by

class Interval:
    def __init__(self, l, r) -> None:
        self.l, self.r = l, r

    def __repr__(self) -> str:
        match (self.l, self.r):
            case (l, r) if l < r: return f"[{l}..={r}]"
            case (l, r) if l == r: return f"{{{l}}}"

    def try_yield(l, r):
        if l <= r:
            yield Interval(l, r)

    def difference(self, other):
        if isinstance(other, Interval):
            match (self.l, self.r, other.l, other.r):
                case (l1, r1, l2, r2) if r1 < l2: # 2 is non-overlapping to the left
                    yield Interval(l1, r1)
                case (l1, r1, l2, r2) if l1 > r2: # 2 is non-overlapping to the right
                    yield Interval(l1, r1)
                case (l1, r1, l2, r2) if l1 <= l2 and r1 >= r2: # 1 fully overlaps 2
                    yield from Interval.try_yield(l1, l2 - 1)
                    yield from Interval.try_yield(r2 + 1, r1)
                case (l1, r1, l2, r2) if l2 <= l1 and r2 >= r1: pass  # 2 fully overlaps 1
                case (l1, r1, l2, r2) if l1 <= l2 and r1 >= l2: # 1 and 2 partially overlaps to the right
                    yield from Interval.try_yield(l1, l2 - 1)
                case (l1, r1, l2, r2) if l2 <= l1 and r2 >= l1: # 1 and 2 partially overlaps to the left
                    yield from Interval.try_yield(r2 + 1, r1)
        elif isinstance(other, int):
            yield from self.difference(Interval(other, other))
        else:
            raise NotImplementedError()

def calculate_part1(file: str, row):
    occupied, beacons = set(), set()
    for sx, sy, bx, by in parse(file):
        if by == row:
            beacons.add(bx)
        dist_to_b = abs(bx - sx) + abs(by - sy)
        if row >= sy - dist_to_b and row <= sy + dist_to_b:
            dist_to_r = dist_to_b - abs(sy - row)
            occupied.update(_ for _ in range(sx - dist_to_r, sx + dist_to_r + 1))
    occupied.difference_update(beacons)
    return len(occupied)

def search(file: str, size: int):
    sensors = [_ for _ in parse(file)]
    for row in range(size):
        available = [Interval(0, size)]
        for sx, sy, bx, by in sensors:
            if by == row:
                available = [diff for interval in available for diff in interval.difference(bx)]
            dist_to_b = abs(bx - sx) + abs(by - sy)
            if row >= sy - dist_to_b and row <= sy + dist_to_b:
                dist_to_r = dist_to_b - abs(sy - row)
                span = Interval(sx - dist_to_r, sx + dist_to_r)
                available = [diff for interval in available for diff in interval.difference(span)]
        match available:
            case []: continue
            case [interval] if interval.l == interval.r: return (row, interval.l)
            case _: raise Exception("Unhandled")

def calculate_part2(file: str, size: int):
    (y, x) = search(file, size)
    return 4_000_000 * x + y
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 15, part 1: {}".format(calculate_part1(file, 2_000_000)))
    print("Dec 15, part 2: {}".format(calculate_part2(file, 4_000_000)))
