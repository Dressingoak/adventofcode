import sys
sys.path.append('../')
from puzzle import Puzzle

def parse_forest(file: str):
    trees = []
    with open(file, "r") as f:
        for line in f.readlines():
            trees.append([int(v) for v in line.strip()])
    rows, cols = len(trees), len(trees[0])
    return trees, rows, cols

def calculate_part1(file: str):
    trees, rows, cols = parse_forest(file)
    visible = 2 * rows + 2 * cols - 4 # edge count
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            h = trees[i][j]
            match trees[i][j]:
                case h if h > max(trees[i][l] for l in range(0, j)): visible += 1
                case h if h > max(trees[i][l] for l in range(j + 1, cols)): visible += 1
                case h if h > max(trees[k][j] for k in range(0, i)): visible += 1
                case h if h > max(trees[k][j] for k in range(i + 1, rows)): visible += 1
    return visible

def directional_scenic_score(h: int, lst):
    s = 0
    for v in iter(lst):
        if v < h:
            s += 1
        else:
            return s + 1
    return s

def calculate_part2(file: str):
    trees, rows, cols = parse_forest(file)
    m = 0
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            h = trees[i][j]
            s = 1
            s *= directional_scenic_score(h, [trees[i][l] for l in range(j - 1, -1, -1)])
            s *= directional_scenic_score(h, [trees[i][l] for l in range(j + 1, cols)])
            s *= directional_scenic_score(h, [trees[k][j] for k in range(i - 1, -1, -1)])
            s *= directional_scenic_score(h, [trees[k][j] for k in range(i + 1, rows)])
            m = max(m, s)
    return m
    
puzzle = Puzzle(__file__)

puzzle.add_part(1, calculate_part1)
puzzle.add_part(2, calculate_part2)

if __name__ == '__main__':
    puzzle.run()
