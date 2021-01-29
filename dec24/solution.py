import re

class HexagonTile:

    def __init__(self, ins="", x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        if len(ins) > 0:
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

    def copy(self):
        return HexagonTile("", self.x, self.y, self.z)

    def get_adjacent(self):
        lst = []
        for d in ["e", "se", "sw", "w", "nw", "ne"]:
            tile = self.copy()
            tile.move(d)
            lst.append(tile)
        return set(lst)

floor = set()

for line in open("input.txt").read().strip().split("\n"):
    tile = HexagonTile(line)
    if tile in floor:
        floor.remove(tile)
    else:
        floor.add(tile)

print("Part 1: {}".format(len(floor)))

for i in range(100):
    black = {_ for _ in floor}
    white_neighbours = set().union(*[tile.get_adjacent() for tile in floor]).difference(black)

    new_floor = set()
    for tile in black:
        n = len(tile.get_adjacent().intersection(black))
        if n == 0 or n > 2:
            continue
        new_floor.add(tile)
    for tile in white_neighbours:
        n = len(tile.get_adjacent().intersection(black))
        if n == 2:
            new_floor.add(tile)
    
    floor = new_floor
    # print("Day {}: {}".format(i+1, len(floor)))

print("Part 2: {}".format(len(floor)))
