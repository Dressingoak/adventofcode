known = {}


def find_arrangements(row: str, groups: list[int], indent: int = 0):
    if (seq := row.strip("."), t := tuple(groups)) in known:
        return known[(seq, t)]
    n, m = len(seq), len(groups)
    if m == 0:
        if n == 0 or seq.count("#") == 0:
            known[(seq, t)] = 1
            return 1
        else:
            known[(seq, t)] = 0
            return 0
    first, rest = groups[0], groups[1:]
    free = n - (sum(rest) + len(rest)) - (first - 1)
    count = 0
    for i in range(free):
        if "." in seq[i : i + first] or (
            seq[i + first] == "#" if i + first < n else False
        ):
            continue
        if "#" in seq[:i]:
            break
        count += find_arrangements(seq[i + first + 1 :], rest, indent + 2)

    known[(seq, t)] = count
    return count


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            row, groups = line.strip().split(" ")
            groups = [int(_) for _ in groups.split(",")]
            sum += find_arrangements(row, groups)
    return sum


def part2(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            row, groups = line.strip().split(" ")
            groups = [int(_) for _ in groups.split(",")]
            sum += find_arrangements("?".join([row] * 5), groups * 5)
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
