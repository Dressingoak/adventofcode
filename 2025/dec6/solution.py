def part1(file: str):
    mat = []
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip().split()
            if line[0] == "*" or line[0] == "+":
                operators = [_ for _ in line]
                break
            else:
                mat.append([int(_) for _ in line])
    n, m = len(mat), len(mat[0])
    s = 0
    for j in range(m):
        if operators[j] == "+":
            s += sum(mat[i][j] for i in range(n))
        else:
            p = 1
            for i in range(n):
                p *= mat[i][j]
            s += p
    return s



if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
