import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def roll(v): return (v[0],v[2],-v[1])
def turn(v): return (-v[1],v[0],v[2])
def sequence(v):
    for _ in range(2):
        for _ in range(3):
            v = roll(v)
            yield v
            for i in range(3):
                v = turn(v)
                yield v
        v = roll(turn(roll(v)))

class Scanner:
    def __init__(self, id: int, beacons: list[tuple[int, int, int]]) -> None:
        self.id = id
        self.beacons = beacons
    
    def __repr__(self) -> str:
        return "Scanner<{}, {}>".format(self.id, self.beacons)

    def permutations(self):
        for x in zip(*map(lambda v: sequence(v), self.beacons)):
            yield Scanner(self.id, list(x))

def read(file: str) -> list[Scanner]:
    f = open(file, "r")
    r_id = re.compile('--- scanner (\d+) ---')
    r_beacon = re.compile('(-*\d+),(-*\d+),(-*\d+)')
    id = None
    beacons = []
    scanners = []
    for line in map(lambda x: x.strip(), f.readlines()):
        if line == "":
            scanners.append(Scanner(id, beacons))
            beacons = []
            continue
        m_id = r_id.match(line)
        if m_id is not None:
            id = int(m_id.group(1))
            continue
        m_beacon = r_beacon.match(line)
        beacons.append(tuple(map(lambda x: int(x), list(m_beacon.group(1, 2, 3)))))
    scanners.append(Scanner(id, beacons))
    return scanners

def compute(data: list[Scanner]):
    if len(data) == 1:
        return data[0]
    else:
        print("Remaining scanners: {}".format(len(data)))
    for i, s in enumerate(data):
        m = set(s.beacons)
        for j, t in enumerate(data[(i+1):]):
            for p in t.permutations():
                for v in s.beacons:
                    for w in p.beacons:
                        d = (v[0] - w[0], v[1] - w[1], v[2] - w[2])
                        n = set(map(lambda b: (b[0] + d[0], b[1] + d[1], b[2] + d[2]), p.beacons))
                        I = m.intersection(n)
                        if len(I) >= 12:
                            return compute([Scanner(s.id, list(m.union(n)))] + [r for q, r in enumerate(data) if q != i and q != j + i + 1])

data = read(file)

print("Dec 19, part 1: {}".format(len(compute(data).beacons)))
