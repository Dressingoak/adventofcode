import re

input_data = list(map(lambda x: x.strip(), open("input.txt").readlines()))

class BinarySpacePartitioning:

    def __init__(self, size: int, lower: str, upper: str):
        self.size = size
        self.lower = lower
        self.upper = upper
    
    def get(self, input: str) -> int:
        if len(input) != self.size:
            raise Exception("Input should be of lenght {}.".format(self.size))
        minimum = 0
        inv = list(range(self.size, 0, -1))
        for i in range(self.size):
            if input[i] == self.upper:
                minimum += 2**inv[i] // 2
            elif input[i] == self.lower:
                pass
            else:
                raise Exception("Character '{}' not allowed.".format(input[i]))
        return minimum

class Seat:

    row_finder = BinarySpacePartitioning(7, "F", "B")
    col_finder = BinarySpacePartitioning(3, "L", "R")

    def __init__(self, seat: str):
        m = re.match(r'^([FB]{7})([LR]{3})$', seat)
        self.seat = m.group(0)
        self.row = self.row_finder.get(m.group(1))
        self.col = self.col_finder.get(m.group(2))

    def get_id(self):
        return self.row * 8 + self.col
    
    def __str__(self):
        return "Seat '{}' [row: {}, col: {}]".format(self.seat, self.row, self.col)

print("Part 1: {}".format(max(Seat(_).get_id() for _ in input_data)))

ids = sorted([Seat(_).get_id() for _ in input_data])

for i in range(0, len(ids)):
    if ids[i] + 2 == ids[i+1]:
        print("Part 2: {}".format(ids[i] + 1))
        break
