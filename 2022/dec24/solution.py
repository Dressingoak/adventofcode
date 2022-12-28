import sys
sys.path.append('../')
from path_finding import a_star

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a%b
    return a

def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)

class Blizzards:
    def __init__(self, field, width, height, start, end):
        self.field = field
        self.width = width
        self.height = height
        self.period = lcm(width, height)
        self.start = start
        self.end = end

    def parse(file: str):
        field = []
        height = -2
        with open(file, "r") as f:
            for i, line in enumerate(f.readlines()):
                for j, c in enumerate(line.rstrip()):
                    match c:
                        case ">": field.append((0, j, -i))
                        case "v": field.append((1, j, -i))
                        case "<": field.append((2, j, -i))
                        case "^": field.append((3, j, -i))
                height += 1
            width = len(line.rstrip()) - 2
        start, end = (0, height), (j-2, height-i)
        return Blizzards([(dir, x-1, height+y) for (dir, x, y) in field], width, height, start, end)

    def get_blizzards(self, t):
        positions = set()
        for (dir, x, y) in self.field:
            match dir:
                case 0: positions.add(((x+t) % self.width, y))
                case 1: positions.add((x, (y-t) % self.height))
                case 2: positions.add(((x-t) % self.width, y))
                case 3: positions.add((x, (y+t) % self.height))
        return positions

    def get_next_states(self, state: tuple[int, int, int, int]):
        match state:
            case (time, x, y):
                explore = [(x+dx, y+dy) for dx in range(-1,2) for dy in range(-1,2) if abs(dx)+abs(dy) <= 1]
                explore = [(x, y) for (x, y) in explore if x in range(0, self.width) and y in range(0, self.height)]
                match state:
                    case (_, x, y) if (x, y) == self.start or (x, y) == self.end:
                        explore.append((x, y))
                    case (_, x, y) if (x, y+1) == self.start:
                        explore.append((x, y+1))
                    case (_, x, y) if (x, y-1) == self.end:
                        explore.append((x, y-1))
                blizzards = self.get_blizzards(time)
                for (x, y) in explore:
                    if (x, y) in blizzards:
                        continue
                    yield ((time+1) % self.period, x, y), 1

    def navigate(self, time, start, end):
        match start, end:
            case (sx, sy), (ex, ey):
                s = (time, sx, sy)
                e = lambda s: (s[1], s[2]) == (ex, ey)
                h = lambda s: abs(ex - s[1]) + abs(ey - s[2])
                return a_star(self.get_next_states, s, e, h)

def calculate_part1(file: str):
    blizzards = Blizzards.parse(file)
    _, c = blizzards.navigate(0, blizzards.start, blizzards.end)
    return c - 1

def calculate_part2(file: str):
    blizzards = Blizzards.parse(file)
    (t1, _, _), c1 = blizzards.navigate(0, blizzards.start, blizzards.end)
    (t2, _, _), c2 = blizzards.navigate(t1, blizzards.end, blizzards.start)
    _, c3 = blizzards.navigate(t2, blizzards.start, blizzards.end)
    return (c1 - 1) + c2 + c3

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 24, part 1: {}".format(calculate_part1(file)))
    print("Dec 24, part 2: {}".format(calculate_part2(file)))
