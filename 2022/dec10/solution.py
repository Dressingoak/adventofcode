import sys
sys.path.append('../')
from timing import print_timing

def cpu(file: str):
    cycle = 0
    X = 1
    with open(file, "r") as f:
        for line in f.readlines():
            cycle += 1
            yield (cycle, X)
            match line.strip().split():
                case ["noop"]: pass
                case ["addx", v]:
                    cycle += 1
                    yield (cycle, X)
                    X += int(v)

@print_timing
def calculate_part1(file: str):
    return sum(cycle * X for cycle, X in cpu(file) if cycle % 40 - 20 == 0)

@print_timing
def calculate_part2(file: str):
    s = ""
    for cycle, X in cpu(file):
        pos = (cycle - 1) % 40
        if pos == 0:
            s += "\n"
        s += "#" if pos >= X - 1 and pos < X + 2 else "."
    return s
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 10, part 1: {} (took {})".format(*calculate_part1(file)))
    print("Dec 10, part 2: {} (took {})".format(*calculate_part2(file)))
