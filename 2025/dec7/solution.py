def part1(file: str):
    beams = set()
    splits = 0
    with open(file, "r") as f:
        for line in f.readlines():
            beams_next = set()
            for i, char in enumerate(line.strip()):
                match char:
                    case "S":
                        beams_next.add(i)
                    case "^":
                        if i in beams:
                            beams_next.update((i - 1, i + 1))
                            splits += 1
                    case _:
                        if i in beams:
                            beams_next.add(i)
            beams = beams_next
    return splits


timelines = {}


def paths(i: int, j: int, beams: dict[int, set[int]]):
    if (p := timelines.get((i, j))) is not None:
        return p
    if i in beams and j in beams[i]:
        timelines[(i, j)] = (
            p := (paths(i + 1, j - 1, beams) + paths(i + 1, j + 1, beams))
        )
        return p
    elif i > max(beams.keys()):
        timelines[(i, j)] = 1
        return 1
    else:
        timelines[(i, j)] = (p := paths(i + 1, j, beams))
        return p


def part2(file: str):
    beams = {}
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, char in enumerate(line.strip()):
                match char:
                    case "S":
                        start = (i, j)
                    case "^":
                        if i in beams:
                            beams[i].add(j)
                        else:
                            beams[i] = set((j,))
    return paths(*start, beams)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
