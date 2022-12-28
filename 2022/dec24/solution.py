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
        self.waypoints = [end]
        self.add_waypoint()

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

    def add_waypoint(self, waypoint: tuple[int, int] | None = None):
        match waypoint:
            case None: pass
            case point: self.waypoints.insert(-1, point)

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
            case (trip, time, x, y):
                explore = [(x+dx, y+dy) for dx in range(-1,2) for dy in range(-1,2) if abs(dx)+abs(dy) <= 1]
                explore = [(x, y) for (x, y) in explore if x in range(0, self.width) and y in range(0, self.height)]
                match state:
                    case (_, _, x, y) if (x, y) == self.start or (x, y) == self.end:
                        explore.append((x, y))
                    case (_, _, x, y) if (x, y+1) == self.start:
                        explore.append((x, y+1))
                    case (_, _, x, y) if (x, y-1) == self.end:
                        explore.append((x, y-1))
                blizzards = self.get_blizzards(time)
                for (x, y) in explore:
                    if (x, y) in blizzards:
                        continue
                    if (x, y) == self.waypoints[trip]:
                        yield (trip+1, (time+1) % self.period, x, y), 1
                    else:
                        yield (trip, (time+1) % self.period, x, y), 1

    def terminate(self, state):
        match state:
            case (trip, _, x, y):
                return trip == len(self.waypoints) and (x, y) == self.end

    def estimate(self, state: tuple[int, int, int, int]):
        match state:
            case (trip, _, x, y):
                lst = [(x, y)] + self.waypoints[trip:]
                return sum(abs(lst[i+1][0] - lst[i][0]) + abs(lst[i+1][1] - lst[i][1]) for i in range(len(lst) - 1))

    def navigate(self):
        match self.start:
            case (x, y):
                s = (0, 0, x, y)
                return a_star(self.get_next_states, s, self.terminate, self.estimate)

def calculate_part1(file: str):
    blizzards = Blizzards.parse(file)
    return blizzards.navigate() - 1

def calculate_part2(file: str):
    blizzards = Blizzards.parse(file)
    blizzards.add_waypoint(blizzards.end)
    blizzards.add_waypoint(blizzards.start)
    return blizzards.navigate() - 1

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 24, part 1: {}".format(calculate_part1(file)))
    print("Dec 24, part 2: {}".format(calculate_part2(file)))
