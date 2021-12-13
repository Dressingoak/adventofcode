import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

class Dot:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return "Dot<{}, {}>".format(self.x, self.y)
    
    def fold_vertical(self, x: int):
        if self.x < x:
            return Dot(self.x, self.y)
        elif self.x > x:
            return Dot(2 * x - self.x, self.y)
        else:
            raise Exception("Cannot fold vertical at x={} for dot {}.".format(x, self))
    
    def fold_horizontal(self, y: int):
        if self.y < y:
            return Dot(self.x, self.y)
        elif self.y > y:
            return Dot(self.x, 2 * y - self.y)
        else:
            raise Exception("Cannot fold vertical at y={} for dot {}.".format(y, self))

def read(file: str) -> tuple[Dot, str]:
    re_dots = re.compile('(\d+),(\d+)')
    re_fold = re.compile('fold along (\w)=(\d+)')
    get_dots = True
    f = open(file, "r")
    dots = set()
    fold_instructions = []
    for line in map(lambda x: x.strip(), f.readlines()):
        if line == "":
            get_dots = False
            continue
        if get_dots:
            m = re_dots.match(line)
            if m is not None:
                x, y = m.group(1, 2)
                dots.add(Dot(int(x), int(y)))
            else:
                raise Exception("Could not parse dot from line: '{}'".format(line))
        else:
            m = re_fold.match(line)
            if m is not None:
                d, p = m.group(1, 2)
                fold_instructions.append((d, int(p)))
            else:
                raise Exception("Could not parse fold instruction from line: '{}'".format(line))
    return (dots, fold_instructions)

def fold(dots: set[Dot], fold_instruction: tuple[str, int]):
    folded = set()
    d, p = fold_instruction
    match d:
        case 'x': return set(dot.fold_vertical(p) for dot in dots)
        case 'y': return set(dot.fold_horizontal(p) for dot in dots)
        case _: raise Exception("Unknown folding dimension: '{}'".format(d))

def fold_all(dots: set[Dot], fold_instructions: list[tuple[str, int]]):
    for fold_instruction in fold_instructions:
        dots = fold(dots, fold_instruction)
    return dots

def print_dots(dots: set[Dot]) -> str:
    width = max(d.x for d in dots) + 1
    height = max(d.y for d in dots) + 1
    paper = [["." for _ in range(width)] for _ in range(height)]
    for dot in dots:
        paper[dot.y][dot.x] = "#"
    return "\n".join("".join(row) for row in paper)

dots, fold_instructions = read(file)

print("Dec 13, part 1: {}".format(len(fold(dots, fold_instructions[0]))))
print("Dec 13, part 2:\n{}".format(print_dots(fold_all(dots, fold_instructions))))
