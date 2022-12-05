import sys
import re

def parse(file: str):
    crates: dict[int, list[str]] = dict()
    instructions: list[tuple[int, int, int]] = []

    with open(file, "r") as f:
        search_crates = True

        for line in f.readlines():
            if line.strip() == "":
                search_crates == False
            if search_crates:
                pos = 1
                matches = re.finditer(r'(\s(?P<stack>\d)\s)|(\[(?P<crate>\w)\]\s?)|(?P<empty>\s{3,4})', line.rstrip())
                c = 0
                for m in matches:
                    c += 1
                    match (m.group("empty"), m.group("crate"), m.group("stack")):
                        case (_, None, None): # Empty space
                            pos += 1
                        case (None, crate, None): # Crate
                            if pos in crates:
                                crates[pos].append(crate)
                            else:
                                crates[pos] = [crate]
                            pos += 1
                        case (None, None, _): # Stack label
                            if pos not in crates:
                                crates[pos] = []
                if c == 0 and len(crates.values()) > 0:
                    search_crates = False
            else:
                m = re.match(r'move (\d+) from (\d) to (\d)', line)
                (stacks, src, dst) = m.group(1, 2, 3)
                instructions.append((int(stacks), int(src), int(dst)))
        for lst in crates.values():
            lst.reverse()
    return crates, instructions

def calculate_part1(file: str):
    crates, instructions = parse(file)
    for (stacks, src, dst) in instructions:
        for i in range(stacks):
            crate = crates[src].pop()
            crates[dst].append(crate)
    indices = [_ for _ in crates.keys()]
    indices.sort()
    return "".join(crates[i].pop() for i in indices)

def calculate_part2(file: str):
    crates, instructions = parse(file)
    for (stacks, src, dst) in instructions:
        moved = [crates[src].pop() for _ in range(stacks)]
        moved.reverse()
        crates[dst].extend(moved)
    indices = [_ for _ in crates.keys()]
    indices.sort()
    return "".join(crates[i].pop() for i in indices)
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 5, part 1: {}".format(calculate_part1(file)))
    print("Dec 5, part 2: {}".format(calculate_part2(file)))
