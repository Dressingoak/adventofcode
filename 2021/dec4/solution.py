import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

class Board:
    def __init__(self, data: list[list[int]]):
        self.board = [[(_, False) for _ in row] for row in data]
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def mark(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][0] == value:
                    self.board[i][j] = (value, True)

    def unmarked_sum(self):
        return sum([sum(_[0] for _ in row if _[1] == False) for row in self.board])

    def check(self):
        f = lambda field: field[1] is True
        for i in range(self.rows):
            marked = [self.board[i][j][0] for j in range(self.cols) if self.board[i][j][1]]
            if len(marked) == 5:
                return self.unmarked_sum()
        for j in range(self.cols):
            marked = [self.board[i][j][0] for i in range(self.rows) if self.board[i][j][1]]
            if len(marked) == 5:
                return self.unmarked_sum()

def read(file: str):
    f = open(file, "r")
    draws = [int(n) for n in f.readline().split(",")]
    boards = []
    current = None
    for line in f.readlines():
        trimmed = line.strip()
        if trimmed == "":
            if current is not None:
                boards.append(Board(current))
            current = []
        else:
            current.append([int(_) for _ in trimmed.split()])
    boards.append(Board(current))
    return (draws, boards)

def compute(draws: list[int], boards: list[Board]):
    for draw in draws:
        for board in boards:
            board.mark(draw)
        for board in boards:
            result = board.check()
            if result is not None:
                return draw * result

def compute_last(draws: list[int], boards: list[Board]):
    won = [False for _ in boards]
    for draw in draws:
        for board in boards:
            board.mark(draw)
        for (i, board) in enumerate(boards):
            result = board.check()
            if result is not None:
                if all(w for (j, w) in enumerate(won) if j != i) and won[i] == False:
                    return draw * result
                won[i] = True

print("Dec 4, part 1: {}".format(compute(*read(file))))
print("Dec 4, part 2: {}".format(compute_last(*read(file))))
