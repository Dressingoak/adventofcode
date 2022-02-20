import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

class SeaCucumbers:
    def __init__(self, rows: int, cols: int, sea_cucumbers: dict[str, set[tuple[int, int]]]):
        self.rows, self.cols, self.sea_cucumbers = rows, cols, sea_cucumbers

    def move(self):
        heards = [(">", (0, 1)), ("v", (1, 0))]
        moved = 0
        for heard, (dy, dx) in heards:
            nxt = set()
            for (i, j) in self.sea_cucumbers[heard]:
                k, l = (i + dy) % self.rows, (j + dx) % self.cols
                if not any((k, l) in self.sea_cucumbers[h] for h in map(lambda x: x[0], heards)):
                    nxt.add((k, l))
                    moved += 1
                else:
                    nxt.add((i, j))
            self.sea_cucumbers[heard] = nxt
        return moved

def read(file: str) -> SeaCucumbers:
    f = open(file, "r")
    rows = 0
    cols = None
    sea_cucumbers = {"v": set(), ">": set()}
    for i, line in enumerate(map(lambda x: x.strip(), f.readlines())):
        rows += 1
        if cols is None:
            cols = len(line)
        for j, char in enumerate(line):
            if char == ".":
                continue
            sea_cucumbers[char].add((i, j))
    return SeaCucumbers(rows, cols, sea_cucumbers)


data = read(file)

def calculate(sea_cucumbers: SeaCucumbers) -> int:
    step = 1
    while sea_cucumbers.move() > 0:
        step += 1
    return step

print("Dec 25, part 1: {}".format(calculate(data)))
