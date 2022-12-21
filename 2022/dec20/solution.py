import sys
from typing import TypeVar

T = TypeVar("T")

class DoubleLinkedListEntry:
    def __init__(self, before: T, after: T):
        self.before, self.after = before, after

    def __repr__(self) -> str:
        return (self.before, self.after).__repr__()

class DoubleLinkedList:
    def __init__(self, lst):
        self.values: dict[T, DoubleLinkedListEntry] = {}
        self.n = len(lst)
        for i, x in enumerate(lst):
            self.values[x] = DoubleLinkedListEntry(lst[(i-1) % self.n], lst[(i+1) % self.n])

    def __repr__(self) -> str:
        lst = []
        x = [k for i, k in enumerate(self.values.keys()) if i == 0][0]
        for _ in range(self.n):
            lst.append(x[1])
            x = self.values[x].after
        return lst.__repr__()

    def find(self, pred) -> tuple[T, DoubleLinkedListEntry]:
        for k, v in self.values.items():
            if pred(k):
                return k, v
    
    def pop(self, value) -> DoubleLinkedListEntry:
        entry = self.values.pop(value)
        self.values[entry.before].after = entry.after
        self.values[entry.after].before = entry.before
        self.n -= 1
        return entry

    def traverse(self, start: T, steps: int) -> tuple[T, DoubleLinkedListEntry]:
        match steps:
            case 0: return (start, self.values[start])
            case x if x < 0:
                y = start
                for _ in range(abs(x) % self.n):
                    y = self.values[y].before
                return (y, self.values[y])
            case x if x > 0:
                y = start
                for _ in range(x % self.n):
                    y = self.values[y].after
                return (y, self.values[y])

    def move(self, value: T, steps: int):
        if steps == 0:
            return
        popped = self.pop(value)
        if steps > 0:
            key, entry = self.traverse(popped.before, steps)
            between = DoubleLinkedListEntry(key, entry.after)
        else:
            key, entry = self.traverse(popped.after, steps)
            between = DoubleLinkedListEntry(entry.before, key)
        self.values[between.after].before = value
        self.values[between.before].after = value
        self.values[value] = between
        self.n += 1
        return

def extract(numbers: DoubleLinkedList):
    s, (cur, _) = 0, numbers.find(lambda x: x[1] == 0)
    for _ in range(3):
        cur, _ = numbers.traverse(cur, 1000)
        s += cur[1]
    return s

def calculate_part1(file: str):
    original = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            x = int(line.strip())
            original.append((i, x))
    numbers = DoubleLinkedList(original)
    for x in original:
        numbers.move(x, x[1])
    return extract(numbers)

def calculate_part2(file: str):
    original = []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            x = int(line.strip())
            original.append((i, x * 811589153))
    numbers = DoubleLinkedList(original)
    for _ in range(10):
        for x in original:
            numbers.move(x, x[1])
    return extract(numbers)
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 20, part 1: {}".format(calculate_part1(file)))
    print("Dec 20, part 2: {}".format(calculate_part2(file)))
