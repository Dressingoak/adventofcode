def parse(file: str):
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
    return towels, designs


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
    towels, designs = parse(file)

    known = {}
    return sum(find_design(design, towels, known) > 0 for design in designs)


def part2(file: str):
    towels, designs = parse(file)
    known = {}
    return sum(find_design(design, towels, known) for design in designs)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
