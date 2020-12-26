class Cube:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if isinstance(other, Cube):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __lt__(self, other):
        return (self.z, self.y, self.x) < (other.z, other.y, other.x)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return "Cube<{:2d},{:2d},{:2d}>".format(self.x, self.y, self.z)
    
    def get_surrounding(self, include_self=True):
        cubes = []
        I = range(27) if include_self else [_ for _ in range(27) if _ != 13]
        for i in I:
            cubes.append(Cube(self.x + i % 3 - 1, self.y + (i // 3) % 3 - 1, self.z + i // 9 - 1))
        return cubes
        
class CubeField:

    def __init__(self, data):
        self.active = set()
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == "#":
                    self.active.add(Cube(j, i, 0))
        self.ranges = self.calculate_ranges()

    def advance(self):
        possible = set()
        for cube in self.active:
            for c in cube.get_surrounding():
                possible.add(c)
        states = set()
        for cube in sorted(list(possible)):
            count = 0
            adjs = cube.get_surrounding(False)
            for adj in adjs:
                if adj in self.active:
                    # print("[DEBUG] Adjecent cube to {} is {}".format(cube, adj))
                    count += 1
            if cube in self.active:
                if count == 2 or count == 3:
                    states.add(cube)
            else:
                if count == 3:
                    states.add(cube)
        self.active = states
        self.ranges = self.calculate_ranges()

    def layer_to_string(self, layer):
        _str = ""
        for y in range(self.ranges[1][0], self.ranges[1][1] + 1):
            for x in range(self.ranges[0][0], self.ranges[0][1] + 1):
                if Cube(x, y, layer) in self.active:
                    _str += "#"
                else:
                    _str += "."
            _str += "\n"
        return _str.strip()
    
    def __str__(self):
        _str = ""
        for k in range(self.ranges[2][0], self.ranges[2][1] + 1):
            _str += "z = {}\n".format(k)
            _str += self.layer_to_string(k)
            _str += "\n\n"
        return _str.strip()

    def calculate_ranges(self):
        ranges = (
            (min([_.x for _ in self.active]), max([_.x for _ in self.active])),
            (min([_.y for _ in self.active]), max([_.y for _ in self.active])),
            (min([_.z for _ in self.active]), max([_.z for _ in self.active]))
        )
        return ranges

initial_data = open("input.txt").read().strip().split("\n")

cubes = CubeField(initial_data)

for i in range(6):
    cubes.advance()
print("Part 1: {}".format(len(cubes.active)))
