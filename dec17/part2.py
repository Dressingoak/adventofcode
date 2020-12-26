class Cube:

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        if isinstance(other, Cube):
            return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w
        return False

    def __lt__(self, other):
        return (self.w, self.z, self.y, self.x) < (other.w, other.z, other.y, other.x)

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.w))

    def __repr__(self):
        return "Cube<{:2d},{:2d},{:2d}>".format(self.x, self.y, self.z, self.w)
    
    def get_surrounding(self, include_self=True):
        cubes = []
        I = range(81) if include_self else [_ for _ in range(81) if _ != 40]
        for i in I:
            dx = (i // 3**0) % 3 - 1
            dy = (i // 3**1) % 3 - 1
            dz = (i // 3**2) % 3 - 1
            dw = (i // 3**3) % 3 - 1
            cubes.append(Cube(self.x + dx, self.y + dy, self.z + dz, self.w + dw))
        return cubes
        
class CubeField:

    def __init__(self, data):
        self.active = set()
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == "#":
                    self.active.add(Cube(j, i, 0, 0))
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
                    count += 1
            if cube in self.active:
                if count == 2 or count == 3:
                    states.add(cube)
            else:
                if count == 3:
                    states.add(cube)
        self.active = states
        self.ranges = self.calculate_ranges()

    def layer_to_string(self, zlayer, wlayer):
        _str = ""
        for y in range(self.ranges[1][0], self.ranges[1][1] + 1):
            for x in range(self.ranges[0][0], self.ranges[0][1] + 1):
                if Cube(x, y, zlayer, wlayer) in self.active:
                    _str += "#"
                else:
                    _str += "."
            _str += "\n"
        return _str.strip()
    
    def __str__(self):
        _str = ""
        for l in range(self.ranges[3][0], self.ranges[3][1] + 1):
            for k in range(self.ranges[2][0], self.ranges[2][1] + 1):
                _str += "z = {}, w = {}\n".format(k, l)
                _str += self.layer_to_string(k, l)
                _str += "\n\n"
        return _str.strip()

    def calculate_ranges(self):
        ranges = (
            (min([_.x for _ in self.active]), max([_.x for _ in self.active])),
            (min([_.y for _ in self.active]), max([_.y for _ in self.active])),
            (min([_.z for _ in self.active]), max([_.z for _ in self.active])),
            (min([_.w for _ in self.active]), max([_.w for _ in self.active]))
        )
        return ranges

initial_data = open("input.txt").read().strip().split("\n")

cubes = CubeField(initial_data)

for i in range(6):
    cubes.advance()
print("Part 1: {}".format(len(cubes.active)))
