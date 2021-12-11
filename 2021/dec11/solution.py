import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

class Grid:

    def __init__(self, grid: list[list[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def __iter__(self):
        self.i = 0
        self.j = 0
        self.stop = False
        return self

    def __next__(self):
        I = (self.i, self.j)
        self.i = (self.i + 1) % self.rows
        if self.i == 0:
            self.j = (self.j + 1) % self.cols
        if self.stop:
            raise StopIteration
        else:
            if self.i == 0 and self.j == 0:
                self.stop = True
            return I

    def __str__(self) -> str:
        rows = ["".join(map(lambda x: str(x), self.grid[i])) for i in range(self.rows)]
        return "\n".join(rows)

    def flashes(self):
        return {(i, j) for (i, j) in iter(self) if self.grid[i][j] > 9}
    
    def adjacent(self, i, j) -> list[tuple[int, int]]:
        idx = [[(k, l) for l in range(j-1, j+2) if l in range(self.cols)] for k in range(i-1, i+2) if k in range(self.rows)]
        flat = {t for ts in idx for t in ts}
        flat.remove((i, j))
        return flat

    def advance(self):
        for (i, j) in iter(self):
            self.grid[i][j] += 1
        flashes = set()
        diff = -1
        while diff != 0:
            now = self.flashes().difference(flashes)
            diff = len(now)
            for (i, j) in now:
                for (k, l) in self.adjacent(i, j):
                    self.grid[k][l] += 1
            flashes.update(now)
        for (i, j) in flashes:
            self.grid[i][j] = 0
        return len(flashes)

def read(file: str) -> Grid:
    f = open(file, "r")
    grid = [[int(_) for _ in line.strip()] for line in f.readlines()]
    return Grid(grid)

def advance_many(grid: Grid, n: int):
    return sum(grid.advance() for _ in range(n))

grid = read(file)

print("Dec 11, part 1: {}".format(advance_many(grid, 100)))
