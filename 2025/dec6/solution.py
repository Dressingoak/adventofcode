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


def part2(file: str):
    chars = []
    with open(file, "r") as f:
        for line in f.readlines():
            chars.append(line)
    n, m = len(chars), len(chars[0])
    chars_t = []
    for j in range(m):
        chars_t.append([chars[i][j] for i in range(n)])
    s = 0
    operator = None
    ss = None
    for line in chars_t:
        if operator is None:
            operator = line[-1]
            if operator == "+":
                ss = 0
            else:
                ss = 1
        if (r := "".join(line)[:-1].strip()) == "":
            s += ss
            operator = None
            ss = None
            continue
        if operator == "+":
            ss += int(r)
        else:
            ss *= int(r)
    return s


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
