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

def play_with_deterministic_dice(init: dict[int, int]):
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

class Polynomial:
    def __init__(self, coef: list[int]) -> None:
        self.coef = coef
        self.n = len(coef) - 1

    def get(self, i):
        try:
            return self.coef[i]
        except:
            return 0

    def mul(self, other):
        n = self.n + other.n
        return Polynomial([sum(self.get(i - j) * other.get(j) for j in range(i + 1)) for i in range(n + 1)])

    def pow(self, n: int):
        if n == 1:
            return Polynomial([k for k in self.coef])
        else:
            return self.pow(n - 1).mul(self)

def combinations(n: int, m: int) -> dict[int, int]:
    """Number of ways to achieve a specific die sum by throwing n m-sided dice."""
    return {i + n: k for i, k in enumerate(Polynomial([1,]*m).pow(n).coef)}

known = dict()

ways = combinations(3, 3)

def advance(p1, p2, s1, s2) -> tuple[int, int]:
    if (p1, p2, s1, s2) in known:
        return known[(p1, p2, s1, s2)]
    wins = 0
    games = 0
    for roll, n in ways.items():
        np = (p1 + roll) % 10
        ns = s1 + np + 1
        if ns >= 21:
            wins += n
            games += n
        else:
            w, g = advance(p2, np, s2, ns)
            wins += n * (g - w)
            games += n * g
    known[(p1, p2, s1, s2)] = (wins, games)
    return (wins, games)

def play_with_dirac_dice(init: dict[int, int]):
    wins, games = advance(init[1] - 1, init[2] - 1, 0, 0)
    return max(wins, games - wins)

data = read(file)

print("Dec 21, part 1: {}".format(play_with_deterministic_dice(data)))
print("Dec 21, part 2: {}".format(play_with_dirac_dice(data)))
