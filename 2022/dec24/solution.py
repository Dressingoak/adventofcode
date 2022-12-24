import sys
sys.path.append('../')
from path_finding import dijkstra

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
    
    def find_next_paths(self, graph, state):
        time = state[0]
        match state:
            case (_, x, y):
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
        costs = {((time+1) % self.period, x, y): 1 for (x, y) in explore if (x, y) not in blizzards}
        graph[state] = costs
        for next in costs.keys():
            if next in graph:
                continue
            yield next

    def build_paths(self, graph: dict, start: tuple[int, int, int]):
        # maximal_paths = sum(self.width * self.height + 2 - len(self.get_blizzards(t)) for t in range(0, self.period))
        explore = set()
        match start:
            case (t, x, y): explore.add((t, x, y))
        while len(explore) > 0:
            additional = set()
            for state in explore:
                additional.update(_ for _ in self.find_next_paths(graph, state))
            explore = additional
            # print(f"... {int(len(graph) / maximal_paths * 10000) / 100}% done ({len(graph)} / {maximal_paths})")
        return graph

    def navigate(self, graph, time, start, end):
        match start:
            case (x, y):
                self.build_paths(graph, (time, x, y))
                _, costs = dijkstra(graph, (time, x, y), None)
        return min(((t, c) for (t, x, y), c in costs.items() if (x, y) == end), key=lambda z: z[1])

def calculate_part1(file: str, graph={}):
    blizzards = Blizzards.parse(file)
    _, c = blizzards.navigate(graph, 0, blizzards.start, blizzards.end)
    # print(f"    Navigated to the end ({c-1} minutes)")
    return c - 1

def calculate_part2(file: str, graph={}):
    blizzards = Blizzards.parse(file)
    t1, c1 = blizzards.navigate(graph, 0, blizzards.start, blizzards.end)
    # print(f"    Navigated to the end ({c1-1} minutes)")
    t2, c2 = blizzards.navigate(graph, t1, blizzards.end, blizzards.start)
    # print(f"    Navigated to the end ({c2} minutes)")
    _, c3 = blizzards.navigate(graph, t2, blizzards.start, blizzards.end)
    # print(f"    Navigated to the end ({c3} minutes)")
    return (c1-1)+c2+c3
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    graph = {}
    print("Dec 24, part 1: {}".format(calculate_part1(file, graph)))
    print("Dec 24, part 2: {}".format(calculate_part2(file, graph)))
