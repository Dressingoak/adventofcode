import sys

def calculate_part1(file: str):
    trees = []
    with open(file, "r") as f:
        for line in f.readlines():
            trees.append([int(v) for v in line.strip()])
    rows, cols = len(trees), len(trees[0])
    visible = 2 * rows + 2 * cols - 4 # edge count
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            match trees[i][j]:
                case h if h > max(trees[i][l] for l in range(0, j)): visible += 1
                case h if h > max(trees[i][l] for l in range(j + 1, cols)): visible += 1
                case h if h > max(trees[k][j] for k in range(0, i)): visible += 1
                case h if h > max(trees[k][j] for k in range(i + 1, rows)): visible += 1
    return visible

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 8, part 1: {}".format(calculate_part1(file)))
    # print("Dec 8, part 2: {}".format(calculate_part2(file)))
