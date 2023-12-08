def parse(file: str):
    connections = {}
    with open(file, "r") as f:
        for line in f.readlines():
            match line.split():
                case [ins]:
                    instructions = [0 if c == "L" else 1 for c in ins]
                case [start, _, l, r]:
                    connections[start] = (l[1:4], r[:3])
    return instructions, connections


def part1(file: str):
    instructions, connections = parse(file)
    instructions_total = len(instructions)
    i = 0
    node = "AAA"
    while node != "ZZZ":
        node = connections[node][instructions[i % instructions_total]]
        i += 1

    return i


def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def part2(file: str):
    instructions, connections = parse(file)
    instructions_total = len(instructions)
    starts = [node for node in connections.keys() if node.endswith("A")]
    ends = {}
    for start in starts:
        end = {}
        i = 0
        node = start
        explored = False
        while not explored:
            node = connections[node][instructions[i % instructions_total]]
            i += 1
            if node == start and i % instructions_total == 0:
                break
            if node.endswith("Z"):
                if node not in end:
                    end[node] = (i, [])
                else:
                    first = end[node][0]
                    if (i - first) % instructions_total == first % instructions_total:
                        explored = True
                    else:
                        for seen in end[node][1]:
                            if (
                                i - seen
                            ) % instructions_total == first % instructions_total:
                                explored = True
                                break
                    if not explored:
                        end[node][1].append(i)
        ends[start] = end
    cycle = 1
    for node, reps in ends.items():
        match list(reps.values()):
            case [(value, [])]:
                cycle = (cycle * value) // gcd(cycle, value)
            case _:
                raise Exception("Shifted cycles not handled")
    return cycle


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
