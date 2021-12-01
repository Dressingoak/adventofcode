import re
instructions = open("input.txt").read().strip().split("\n")

o = 2 # {0: west, 1: north, 2: east, 3: south}
x = 0
y = 0

for ins in instructions:
    m = re.match(r'^([A-Z])([0-9]+)$', ins)
    if m:
        action = m.group(1)
        value = int(m.group(2))

        if action == "N":
            y += value
        elif action == "S":
            y -= value
        elif action == "E":
            x -= value
        elif action == "W":
            x += value
        elif action == "L":
            o = (o - value // 90) % 4
        elif action == "R":
            o = (o + value // 90) % 4
        elif action == "F":
            if o == 1:
                y += value
            elif o == 3:
                y -= value
            elif o == 2:
                x -= value
            else:
                x += value
        else:
            raise Exception("Unexpected action: {}".format(ins))

print("Part 1: {} (location: {},{})".format(abs(x)+abs(y), x, y))

o = 2 # {0: west, 1: north, 2: east, 3: south}
x = 0
y = 0
xwp = -10
ywp = 1

for ins in instructions:
    m = re.match(r'^([A-Z])([0-9]+)$', ins)
    if m:
        action = m.group(1)
        value = int(m.group(2))

        if action == "N":
            ywp += value
        elif action == "S":
            ywp -= value
        elif action == "E":
            xwp -= value
        elif action == "W":
            xwp += value
        elif action == "L" or action == "R":
            rot = (value * (1 if action == "R" else -1) // 90) % 4
            if rot == 1:
                tmp = xwp
                xwp = -ywp
                ywp = tmp
            elif rot == 2:
                xwp *= -1
                ywp *= -1
            elif rot == 3:
                tmp = ywp
                ywp = -xwp
                xwp = tmp
        elif action == "F":
            sx = value * xwp
            sy = value * ywp
            x += sx
            y += sy
        else:
            raise Exception("Unexpected action: {}".format(ins))
    # print("[DEBUG] Ins: {}, wp: ({}, {}), position: ({}, {})".format(ins, xwp, ywp, x, y))

print("Part 2: {} (location: {},{})".format(abs(x)+abs(y), x, y))
