def find_design(design: str, towels: list[str], known: dict[str, int]):
    if design in known:
        return known[design]
    sd = len(design)
    if sd == 0:
        return 1
    count = 0
    for towel in towels:
        s = len(towel)
        if sd >= s and design[0:s] == towel:
            count += find_design(design[s:], towels, known)
    known[design] = count
    return count


def part1(file: str):
    designs = []

    with open(file, "r") as f:
        parse_designs = False
        for line in f.readlines():
            line = line.strip()
            if line == "":
                parse_designs = True
                continue
            if parse_designs:
                designs.append(line)
            else:
                towels = line.split(", ")

    known = {}
    count = 0
    for i, design in enumerate(designs):
        if find_design(design, towels, known) > 0:
            count += 1
    return count


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
