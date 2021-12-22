import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str):
    r = re.compile('(on|off) x=(-*\d+)\.\.(-*\d+),y=(-*\d+)\.\.(-*\d+),z=(-*\d+)\.\.(-*\d+)')
    f = open(file, "r")
    instructions = []
    for line in map(lambda x: x.strip(), f.readlines()):
        m = r.match(line)
        state = m.group(1)
        x1, x2, y1, y2, z1, z2 = tuple(map(lambda x: int(x), list(m.group(2,3,4,5,6,7))))
        instructions.append((state, x1, x2, y1, y2, z1, z2))
    return instructions

def generate_cubes(x1, x2, y1, y2, z1, z2):
    mi, ma = -50, 50
    for x in range(max(x1, mi), min(x2, ma) + 1):
        for y in range(max(y1, mi), min(y2, ma) + 1):
            for z in range(max(z1, mi), min(z2, ma) + 1):
                yield (x, y, z)

def calculate(data: list[tuple[str, int, int, int, int, int, int]]):
    active = set()
    for state, x1, x2, y1, y2, z1, z2 in data:
        cubes = set(generate_cubes(x1, x2, y1, y2, z1, z2))
        if state == "on":
            active.update(cubes)
        else:
            active.difference_update(cubes)
    return len(active)

data = read(file)

print("Dec 22, part 1: {}".format(calculate(data)))
