import sys
sys.path.append('../')
from puzzle import Puzzle
import re

def parse(file: str):
    crates: dict[int, list[str]] = dict()
    instructions: list[tuple[int, int, int]] = []

    with open(file, "r") as f:
        search_crates = True
        for line in f.readlines():
            if line.strip() == "":
                search_crates = False
                continue
            if search_crates:
                pos = 1
                for i in range(1, len(line), 4):
                    crate = line[i]
                    ascii = ord(crate)
                    if ascii >= 65 and ascii <= 90:
                        if pos in crates:
                            crates[pos].append(crate)
                        else:
                            crates[pos] = [crate]
                    elif ascii >= 40 and ascii <= 57:
                        if pos not in crates:
                            crates[pos] = []
                    pos += 1
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
    
puzzle = Puzzle(__file__)

puzzle.add_part(1, calculate_part1)
puzzle.add_part(2, calculate_part2)

if __name__ == '__main__':
    puzzle.run()
