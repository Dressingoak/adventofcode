import sys

def ceilhalf(x):
    return - (x // -2) if x > 0 else x // 2

def advance_tail(h, t):
    match (h, t):
        case ((hx, hy), (tx, ty)): delta = (hx - tx, hy - ty)
    match delta:
        case (dx, dy) if max(abs(dx), abs(dy)) < 2: return t
        case (dx, dy) if max(abs(dx), abs(dy)) < 3: return (t[0] + ceilhalf(dx), t[1] + ceilhalf(dy))

def calculate(file: str, n: int):
    positions = set()
    rope = [(0, 0), ] * n
    with open(file, "r") as f:
        for line in f.readlines():
            (dir, steps) = line.strip().split(" ")
            match dir:
                case "L": dx, dy = -1, 0
                case "R": dx, dy = 1, 0
                case "U": dx, dy = 0, 1
                case "D": dx, dy = 0, -1
            for _ in range(int(steps)):
                rope[0] = (rope[0][0] + dx, rope[0][1] + dy)
                for i in range(1, n):
                    rope[i] = advance_tail(rope[i-1], rope[i])
                positions.add(rope[-1])
    return len(positions)

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 9, part 1: {}".format(calculate(file, 2)))
    print("Dec 9, part 2: {}".format(calculate(file, 10)))
