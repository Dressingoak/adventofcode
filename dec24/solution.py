import re

class HexagonTile:

    def __init__(self, ins, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.move_many(ins)

    def __repr__(self):
        return "HexagonTile<{}, {}, {}>".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def move_many(self, ins):
        for d in re.finditer(r"(e|se|sw|w|nw|ne)", ins):
            self.move(d.group())

    def move(self, d):
        if d == "e":
            self.x += 1
            self.y -= 1
        elif d == "se":
            self.y -= 1
            self.z += 1
        elif d == "sw":
            self.z += 1
            self.x -= 1
        elif d == "w":
            self.x -= 1
            self.y += 1
        elif d == "nw":
            self.y += 1
            self.z -= 1
        elif d == "ne":
            self.z -= 1
            self.x += 1
        else:
            raise Exception("Unknown hexagon grid direction: {}".format(d))

floor = dict()

for line in open("input.txt").read().strip().split("\n"):
    tile = HexagonTile(line)
    if tile in floor:
        del floor[tile]
    else:
        floor[tile] = 1

print("Part 1: {}".format(len(floor)))
