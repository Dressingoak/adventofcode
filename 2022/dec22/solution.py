import sys

def calculate_part1(file: str):
    grove: list[list[str]] = []
    instructions = []
    read_grove = True
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.rstrip()
            if line == "":
                read_grove = False
                continue
            if read_grove:
                grove.append([_ for _ in line])
            else:
                d = ""
                for c in line:
                    match c:
                        case x if ord(x) >= 48 and ord(x) <= 57:
                            d += x
                        case "R" | "L":
                            if len(d) > 0:
                                instructions.append(int(d))
                                d = ""
                            instructions.append(c)
                        case _: raise Exception("Unhandled")
                if len(d) > 0:
                    instructions.append(int(d))
    facing, i, j = 0, 0, grove[0].index(".")
    for ins in instructions:
        match ins:
            case "L": facing = (facing-1) % 4
            case "R": facing = (facing+1) % 4
            case x if isinstance(x, int):
                remaining = x
                if facing % 2 == 0:
                    row = []
                    for k in range(len(grove[i])):
                        try:
                            row.append(grove[i][k])
                        except IndexError:
                            row.append(" ")
                    n, inc, k = len(row), 1 - facing, j
                    while remaining > 0:
                        k = (k + inc) % n
                        match row[k]:
                            case ".":
                                j = k
                                remaining -= 1
                            case "#":
                                break
                else:
                    column = []
                    for k in range(len(grove)):
                        try:
                            column.append(grove[k][j])
                        except IndexError:
                            column.append(" ")
                    n, inc, k = len(column), 2 - facing, i
                    while remaining > 0:
                        k = (k + inc) % n
                        match column[k]:
                            case ".":
                                i = k
                                remaining -= 1
                            case "#":
                                break
    return 1000 * (i + 1) + 4 * (j + 1) + facing

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 22, part 1: {}".format(calculate_part1(file)))
    # print("Dec 22, part 2: {}".format(calculate_part2(file)))
