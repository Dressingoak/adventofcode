import sys
import re

try:
    file = sys.argv[1]
except:
    file = "input.txt"

def read(file: str):
    r = re.compile("Player (\d+) starting position: (\d)")
    f = open(file, "r")
    return {int(p): int(s) for p, s in [r.match(line).group(1, 2) for line in map(lambda x: x.strip(), f.readlines())]}

def play(init: dict[int, int]):
    die = 0
    player = 0
    scores = [0, 0]
    positions = [init[1] - 1, init[2] - 1]
    total_rolls = 0
    while max(scores) < 1000:
        rolls = 0
        for _ in range(3):
            rolls += die + 1
            die += 1
            die %= 100
        total_rolls += 3
        positions[player] += rolls
        positions[player] %= 10
        scores[player] += positions[player] + 1
        player += 1
        player %= 2
    return total_rolls * scores[player]

data = read(file)

print("Dec 21, part 1: {}".format(play(data)))
