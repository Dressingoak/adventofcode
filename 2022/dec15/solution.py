import sys
import re

def parse(file: str):
    pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    with open(file, "r") as f:
        for line in f.readlines():
            m = re.match(pattern, line.strip())
            sx, sy, bx, by = [int(_) for _ in m.group(1, 2, 3, 4)]
            yield sx, sy, bx, by

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

class Polygon:
    def __init__(self, points):
        self.points = points
    
    def from_sensor_and_beacon(sensor, beacon):
        match (sensor, beacon):
            case ((sx, sy), (bx, by)):
                dist = abs(bx - sx) + abs(by - sy)
                return Polygon([
                    (sx, sy + dist),
                    (sx + dist, sy)
                    (sx, sy - dist)
                    (sx - dist, sy)
                ])

    def diff(self, other):
        

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 15, part 1: {}".format(calculate_part1(file, 2000000)))
    # print("Dec 15, part 2: {}".format(calculate_part2(file)))
