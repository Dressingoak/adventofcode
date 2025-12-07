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


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
