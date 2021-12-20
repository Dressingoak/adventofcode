import sys
import re
import copy

try:
    file = sys.argv[1]
except:
    file = "input.txt"

class SnailfishNumber:
    def __init__(self, left, right, pos) -> None:
        self.left = left
        self.right = right
        self.pos = pos

    def push_pos(self, value):
        self.pos = [value] + self.pos
        if isinstance(self.left, SnailfishNumber):
            self.left.push_pos(value)
        if isinstance(self.right, SnailfishNumber):
            self.right.push_pos(value)

    def __str__(self) -> str:
        return "[{},{}]".format(self.left, self.right)

    def add(self, other):
        l = copy.deepcopy(self)
        l.push_pos(0)
        r = copy.deepcopy(other)
        r.push_pos(1)
        sfn = SnailfishNumber(l, r, [])
        reduced = False
        while not reduced:
            if sfn.explode():
                continue
            if sfn.split():
                continue
            reduced = True    
        return sfn

    def get_all_positions(self):
        positions = set()
        for i, sub in enumerate([self.left, self.right]):
            if isinstance(sub, SnailfishNumber):
                positions.update(sub.get_all_positions())
            else:
                positions.add(tuple(self.pos + [i]))
        return sorted(list(positions))

    def get(self, pos):
        if len(pos) == 1:
            if pos[0] == 0:
                return self.left
            else:
                return self.right
        else:
            if pos[0] == 0:
                return self.left.get(pos[1:])
            else:
                return self.right.get(pos[1:])
    
    def set(self, pos, value):
        if len(pos) == 1:
            if pos[0] == 0:
                self.left = value
            else:
                self.right = value
        else:
            if pos[0] == 0:
                return self.left.set(pos[1:], value)
            else:
                return self.right.set(pos[1:], value)

    def explode(self, level = 1):
        s = None
        for sub in [self.left, self.right]:
            should_break = False
            if isinstance(sub, SnailfishNumber) and level == 4:
                s = copy.deepcopy(sub)
                should_break = True
            elif isinstance(sub, SnailfishNumber) and level < 4:
                q = sub.explode(level + 1)
                if q is not None:
                    should_break = True
                    s = q
            if should_break:
                break
        if level > 1:
            return s
        if s is not None:
            self.set(s.pos, 0)
            all_positions = self.get_all_positions()
            i = all_positions.index(tuple(s.pos))
            if i > 0:
                pos = list(all_positions[i - 1])
                self.set(pos, self.get(pos) + s.left)
            if i < len(all_positions) - 1:
                pos = list(all_positions[i + 1])
                self.set(pos, self.get(pos) + s.right)
            return True
        return False

    def split(self):
        spos, v = None, None
        for pos in self.get_all_positions():
            p = list(pos)
            v = self.get(p)
            if self.get(p) >= 10:
                spos = p
                break
        if spos is not None:
            self.set(spos, SnailfishNumber(v // 2, -(v // -2), spos))
            return True
        return False
    
    def magnitude(self):
        s = 0
        for i, sub in enumerate([self.right, self.left]):
            s += (2 + i) * (sub.magnitude() if isinstance(sub, SnailfishNumber) else sub)
        return s

def parse(number: str, pos: list[int] = []):
    try:
        return int(number)
    except:
        r = re.compile('^\[(\d+),(\d+)\]$')
    m = r.match(number)
    if m is not None:
        l, r = m.group(1, 2)
        return SnailfishNumber(int(l), int(r), pos)
    else:
        c = 0
        for i, char in enumerate(number):
            if char == "[":
                c += 1
            elif char == "]":
                c -= 1
            elif char == "," and c == 1:
                l, r = parse(number[1:i], pos + [0]), parse(number[i+1:-1], pos + [1])
                return SnailfishNumber(l, r, pos)
        raise Exception("Could  not parse number: {}".format(number))

def read(file: str) -> list[SnailfishNumber]:
    f = open(file, "r")
    return [parse(line) for line in map(lambda x: x.strip(), f.readlines())]

def sum_all(data: list[SnailfishNumber]) -> SnailfishNumber:
    s = data[0]
    for r in data[1:]:
        s = s.add(r)
    return s

def largest_pair_magnitude(data: list[SnailfishNumber]):
    n = len(data)
    m = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            m = max(m, data[i].add(data[j]).magnitude())
    return m

data = read(file)

print("Dec 18, part 1: {}".format(sum_all(data).magnitude()))
print("Dec 18, part 2: {}".format(largest_pair_magnitude(data)))
