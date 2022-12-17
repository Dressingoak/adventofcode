import sys

def push_shape(shape: set[tuple[int, int]]) -> list[tuple[int, int]]:
    height = max(k for k, _ in shape) + 1
    return sorted([(height - i - 1, j) for i, j in shape])

def parse_shapes(shape_file: str):
    shapes, shape, i = [], set(), 0
    with open(shape_file, "r") as f:
        for line in f.readlines():
            if line.strip() == "":
                shapes.append(push_shape(shape))
                shape, i = set(), 0
                continue
            shape.update((i, j) for j, c in enumerate(line.strip()) if c == "#")
            i += 1
        shapes.append(push_shape(shape))
    return shapes

def parse_jets(file: str):
    with open(file, "r") as f:
        jets = [-1 if c == "<" else 1 for line in f.readlines() for c in line.strip()]
    return jets

class Chamber:
    def __init__(self, file: str, shape_file: str):
        self.width = 7
        self.height = 0
        self.jets = parse_jets(file) # list of -1 (<) and 1 (>)
        self.jet_index = -1
        self.shapes = parse_shapes(shape_file) # Coordinates for the shapes
        self.shape_index = -1
        self.rocks = [] # Row-major matrix of rock positions

    def get_nearest_below(self, i, j):
        try:
            return max(k for k, c in enumerate(self.rocks[j::(self.width)]) if c == "#" and (k < i if i is not None else True))
        except ValueError:
            return -1
    
    def get_height(self):
        self.height = max(self.get_nearest_below(None, j) for j in range(self.width)) + 1
        return self.height

    def get_nearest_left(self, i, j):
        l, r = i * self.width, (i + 1) * self.width
        try:
            return max(l for l, c in enumerate(self.rocks[l:r]) if c == "#" and l < j)
        except ValueError:
            return -1

    def get_nearest_right(self, i, j):
        l, r = i * self.width, (i + 1) * self.width
        try:
            return min(l for l, c in enumerate(self.rocks[l:r]) if c == "#" and l > j)
        except ValueError:
            return self.width

    def get_next_jet(self):
        self.jet_index += 1
        self.jet_index %= len(self.jets)
        return self.jets[self.jet_index]

    def get_next_rock(self):
        self.shape_index += 1
        self.shape_index %= len(self.shapes)
        height = self.get_height()
        return [(i + height + 3, j + 2) for i, j in self.shapes[self.shape_index]]
    
    def get_nearest_obstacles(self, coords, movement):
        obstacles = set()
        match movement:
            case (-1, 0):
                for i, (k, l) in enumerate(coords):
                    if len([ll for j, (kk, ll) in enumerate(coords) if j != i and ll < l and kk == k]) == 0:
                        obstacles.add((k, self.get_nearest_left(k, l)))
            case (1, 0):
                for i, (k, l) in enumerate(coords):
                    if len([ll for j, (kk, ll) in enumerate(coords) if j != i and ll > l and kk == k]) == 0:
                        obstacles.add((k, self.get_nearest_right(k, l)))
            case (0, -1):
                for i, (k, l) in enumerate(coords):
                    if len([kk for j, (kk, ll) in enumerate(coords) if j != i and kk < k and ll == l]) == 0:
                        obstacles.add((self.get_nearest_below(k, l), l))
        return obstacles

    def set(self, i, j):
        index = i * self.width + j
        size = len(self.rocks)
        if index >= size:
            self.rocks.extend(["." for _ in range(size, index + 1)])
        self.rocks[index] = "#"

    def simulate(self):
        rock = self.get_next_rock()
        while True:
            push = self.get_next_jet()
            obstacles = self.get_nearest_obstacles(rock, (push, 0))
            pushed_rock = [(i, j + push) for i, j in rock]
            if not any((i, j) in obstacles for i, j in pushed_rock):
                rock = pushed_rock
            obstacles = self.get_nearest_obstacles(rock, (0, -1))
            falling_rock = [(i - 1, j) for i, j in rock]
            if not any((i, j) in obstacles for i, j in falling_rock):
                rock = falling_rock
            else:
                break
        for i, j in rock:
            self.set(i, j)

    def visualize(self):
        h = self.get_height() + 2
        arr = ["+-------+"]
        for i in range(h):
            s = "|"
            for j in range(self.width):
                try:
                    s += self.rocks[i * self.width + j]
                except IndexError:
                    s += " "
            s += "|"
            arr.append(s)
        return "\n".join(reversed(arr))

def calculate_part1(file: str, shape_file: str):
    chamber = Chamber(file, shape_file)
    for _ in range(2022):
        chamber.simulate()
    return chamber.get_height()

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"
    try:
        shape_file = sys.argv[2]
    except:
        shape_file = "shapes.txt"

    print("Dec 17, part 1: {}".format(calculate_part1(file, shape_file)))
    # print("Dec 17, part 2: {}".format(calculate_part2(file)))
