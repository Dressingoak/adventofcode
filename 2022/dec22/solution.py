import sys
sys.path.append('../')
from puzzle import Puzzle

def parse(file: str, size: int):
    grove: dict[tuple[int, int], str] = {}
    instructions: list[int | str] = []
    read_grove = True
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.rstrip()
            if line == "":
                read_grove = False
                continue
            if read_grove:
                j = 0
                while j < len(line):
                    row = line[j:(j+size)]
                    if row == " " * size:
                        j += size
                        continue
                    k = (i // size, j // size)
                    if k not in grove:
                        grove[k] = []
                    grove[k].append([_ for _ in row])
                    j += size
            else:
                d = ""
                for c in line:
                    match c:
                        case x if ord(x) >= 48 and ord(x) <= 57:
                            d += x
                        case "R" | "L":
                            if len(d) > 0:
                                instructions.append(int(d))
                                d = ""
                            instructions.append(c)
                        case _: raise Exception("Unhandled")
                if len(d) > 0:
                    instructions.append(int(d))
    return grove, instructions

def patch(grove: dict[tuple[int, int], list[list[str]]]) -> dict[tuple[int, int, int], tuple[int, int, int]]:
    height = max(i for i, _ in grove.keys()) + 1
    width = max(j for _, j in grove.keys()) + 1
    wrapping = {}
    for i, j in grove.keys():
        for side in range(4):
            i_inc = 0 if side % 2 == 0 else 2 - side
            j_inc = 0 if side % 2 == 1 else 1 - side
            c = 1
            while True:
                k = ((i + c * i_inc) % height, (j + c * j_inc) % width)
                if k in grove:
                    wrapping[(i, j, side)] = (k[0], k[1], (side + 2) % 4)
                    break
                else:
                    c += 1
    return wrapping

class Vector:
    def __init__(self, data):
        self.data = data

    def __add__(self, other):
        return Vector([x + y for x, y in zip(self.data, other.data)])

    def __sub__(self, other):
        return Vector([x - y for x, y in zip(self.data, other.data)])

    def __repr__(self) -> str:
        return self.data.__repr__()

class Matrix:
    def __init__(self, data):
        self.data = data

    def __repr__(self) -> str:
        return self.data.__repr__()

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector([sum(x * y for x, y in zip(row, other.data)) for row in self.data])

    def sin(n: int): return [0, 1, 0, -1][n % 4]
    def cos(n: int): return Matrix.sin(n + 1)

    def rotX(n):
        return Matrix([
            [1,             0,              0],
            [0, Matrix.cos(n), -Matrix.sin(n)],
            [0, Matrix.sin(n),  Matrix.cos(n)],
        ])

    def rotY(n):
        return Matrix([
            [ Matrix.cos(n), 0, Matrix.sin(n)],
            [             0, 1,             0],
            [-Matrix.sin(n), 0, Matrix.cos(n)],
        ])

    def rotZ(n):
        return Matrix([
            [Matrix.cos(n), -Matrix.sin(n), 0],
            [Matrix.sin(n),  Matrix.cos(n), 0],
            [            0,              0, 1]
        ])

class Face:
    def __init__(self, id, tl: Vector, tr: Vector, br: Vector, bl: Vector, connected: dict):
        self.id = id
        self.points = [tl, tr, br, bl]
        self.connected = connected

    def __repr__(self) -> str:
        return f"Face<{self.id}, {self.points}>"

    def translate(self, offset: Vector):
        points = [p + offset for p in self.points]
        self.points = points

    def rotate(self, offset: Vector, mat: Matrix):
        points = [mat * (p - offset) + offset for p in self.points]
        self.points = points

    def find_connected(self, faces, direction = None, skip = None):
        for dir, next in self.connected.items():
            if direction is not None and direction != dir:
                continue
            if next == skip:
                continue
            yield (self.id, dir, next)
            yield from faces[next].find_connected(faces, None, self.id)

def patch_cube(grove: dict[tuple[int, int], list[list[str]]]) -> dict[tuple[int, int, int], tuple[int, int, int]]:
    faces: dict[tuple[int, int], Face] = {}
    rot = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i, j in grove.keys():
        face = Face(
            (i, j),
            Vector([i,     j + 1, 0]),
            Vector([i + 1, j + 1, 0]),
            Vector([i + 1, j,     0]),
            Vector([i,     j,     0]),
            {r: (k, l) for r, (k, l) in enumerate([(i + di, j + dj) for di, dj in rot]) if (k, l) in grove}
        )
        faces[(i, j)] = face
    i, j = 0, 0
    found = False
    while not found:
        if (i, j) not in grove:
            j += 1
        else:
            found = True
    for face in faces.values():
        face.translate(Vector([-i, -j, 0]))
    for src, dir, dst in faces[(i, j)].find_connected(faces):
        p2, p1 = faces[src].points[(dir + 1) % 4], faces[src].points[dir]
        match (p1.data, p2.data):
            case ([x1, x2, x3], [y1, y2, y3]) if x1 == y1 and x2 == y2 and x3 != y3: offset = Vector([x1, x2,  0])
            case ([x1, x2, x3], [y1, y2, y3]) if x1 == y1 and x2 != y2 and x3 == y3: offset = Vector([x1,  0, x3])
            case ([x1, x2, x3], [y1, y2, y3]) if x1 != y1 and x2 == y2 and x3 == y3: offset = Vector([ 0, x2, x3])
        normal = p2 - p1
        match normal.data:
            case [n, 0, 0]: mat = Matrix.rotX(n)
            case [0, n, 0]: mat = Matrix.rotY(n)
            case [0, 0, n]: mat = Matrix.rotZ(n)
        to_rotate = set(key for _, _, key in faces[src].find_connected(faces, dir))
        for id in to_rotate:
            faces[id].rotate(offset, mat)

    wrapping = {}
    for (i, j), face in faces.items():
        for side in range(4):
            edge = (face.points[side], face.points[(side + 1) % 4])
            for (k, l), neighbor in faces.items():
                if (k, l) == (i, j):
                    continue
                for other_side in range(3, -1, -1):
                    other_edge = (neighbor.points[(other_side + 1) % 4], neighbor.points[other_side])
                    match (edge, other_edge):
                        case ((p1, p2), (q1, q2)) if p1.data == q1.data and p2.data == q2.data:
                            wrapping[(i, j, side)] = (k, l, other_side)
    return wrapping

def rotate(i, j, size, n):
    match n:
        case 0: return (i, j)
        case n if n > 0:
            ip, jp = -j + (size - 1), i
            return rotate(ip, jp, size, n-1)
        case n if n < 0:
            ip, jp = j, -i + (size - 1)
            return rotate(ip, jp, size, n+1)

def walk(grove: dict[tuple[int, int], list[list[str]]], instructions: list[int | str], size: int, patching: dict[tuple[int, int, int], tuple[int, int, int]]):
    facing, i, ii, jj = 0, 0, 0, 0
    found = False
    while not found:
        if (ii, jj) not in grove:
            jj += 1
        else:
            j = grove[(ii, jj)][i].index(".")
            found = True
    for ins in instructions:
        match ins:
            case "L": facing = (facing-1) % 4
            case "R": facing = (facing+1) % 4
            case x if isinstance(x, int):
                remaining = x
                while remaining > 0:
                    try: # Walk in the current patch, except if trying to leave
                        i_inc = 0 if facing % 2 == 0 else 2 - facing
                        j_inc = 0 if facing % 2 == 1 else 1 - facing
                        k, l = i + i_inc, j + j_inc
                        if k < 0 or k == size or l < 0 or l == size:
                            raise IndexError()
                        match grove[(ii, jj)][k][l]:
                            case ".":
                                i, j = k, l
                                remaining -= 1
                            case "#":
                                break
                    except IndexError: # Find the connected patch
                        wii, wjj, side = patching[(ii, jj, facing)]
                        wfacing = (side + 2) % 4
                        i_inc = 0 if wfacing % 2 == 0 else 2 - wfacing
                        j_inc = 0 if wfacing % 2 == 1 else 1 - wfacing
                        k, l = rotate(i, j, size, facing - wfacing)
                        k -= (size - 1) * i_inc
                        l -= (size - 1) * j_inc
                        match grove[(wii, wjj)][k][l]:
                            case ".":
                                facing = wfacing
                                ii, jj = wii, wjj
                                i, j = k, l
                                remaining -= 1
                            case "#":
                                break
    return 1000 * (ii * size + i + 1) + 4 * (jj * size + j + 1) + facing

def calculate_part1(file: str, size: int = 50):
    grove, instructions = parse(file, size)
    patching = patch(grove)
    return walk(grove, instructions, size, patching)

def calculate_part2(file: str, size: int = 50):
    grove, instructions = parse(file, size)
    patching = patch_cube(grove)
    return walk(grove, instructions, size, patching)

if __name__ == '__main__':

    puzzle = Puzzle(__file__)

    puzzle.add_part(1, calculate_part1)
    puzzle.add_part(2, calculate_part2)
    puzzle.set_parameter_help("size", "map patch size")

    puzzle.run()
