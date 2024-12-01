def part1(file: str):
    sum = 0
    l1, l2 = [], []
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = line.split()
            l1.append(int(e1))
            l2.append(int(e2))
    l1.sort()
    l2.sort()
    for e1, e2 in zip(l1, l2):
        sum += abs(e1 - e2)
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
