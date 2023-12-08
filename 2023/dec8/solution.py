def part1(file: str):
    connections = {}
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split():
                case [ins]:
                    instructions = [0 if c == "L" else 1 for c in ins]
                case [start, _, l, r]:
                    connections[start] = (l[1:4], r[:3])

    instructions_total = len(instructions)
    i = 0
    node = "AAA"
    while node != "ZZZ":
        node = connections[node][instructions[i % instructions_total]]
        i += 1

    return i


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
