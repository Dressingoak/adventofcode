import sys

def parse(file: str, size: int):
    grove: dict[tuple[int, int], str] = {}
    instructions: list[int | str] = []
    read_grove = True
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.rstrip()
            if line == "":
                read_grove = False
                continue
            if read_grove:
                j = 0
                while j < len(line):
                    row = line[j:(j+size)]
                    if row == " " * size:
                        j += size
                        continue
                    k = (i // size, j // size)
                    if k not in grove:
                        grove[k] = []
                    grove[k].append([_ for _ in row])
                    j += size
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
    return grove, instructions

def patch(grove: dict[tuple[int, int], list[list[str]]]) -> dict[tuple[int, int, int], tuple[int, int, int]]:
    height = max(i for i, _ in grove.keys()) + 1
    width = max(j for _, j in grove.keys()) + 1
    wrapping = {}
    for i, j in grove.keys():
        for side in range(4):
            i_inc = 0 if side % 2 == 0 else 2 - side
            j_inc = 0 if side % 2 == 1 else 1 - side
            c = 1
            while True:
                k = ((i + c * i_inc) % height, (j + c * j_inc) % width)
                # print(f"Testing: {k}")
                if k in grove:
                    wrapping[(i, j, side)] = (k[0], k[1], (side + 2) % 4)
                    break
                else:
                    c += 1
    return wrapping

def rotate(i, j, size, n):
    match n:
        case 0: return i, j
        case _:
            ip, jp = -j + size, i
            return rotate(ip, jp, size, n-1)

def walk(grove: dict[tuple[int, int], list[list[str]]], instructions: list[int | str], size: int, patching: dict[tuple[int, int, int], tuple[int, int, int]]):
    facing, i, ii, jj = 0, 0, 0, 0
    found = False
    while not found:
        if (ii, jj) not in grove:
            jj += 1
        else:
            j = grove[(ii, jj)][i].index(".")
            found = True
    for ins in instructions:
        match ins:
            case "L": facing = (facing-1) % 4
            case "R": facing = (facing+1) % 4
            case x if isinstance(x, int):
                remaining = x
                while remaining > 0:
                    try:
                        i_inc = 0 if facing % 2 == 0 else 2 - facing
                        j_inc = 0 if facing % 2 == 1 else 1 - facing
                        k, l = i + i_inc, j + j_inc
                        if k < 0 or k == size or l < 0 or l == size:
                            raise IndexError()
                        match grove[(ii, jj)][k][l]:
                            case ".":
                                i, j = k, l
                                remaining -= 1
                            case "#":
                                break
                    except IndexError:
                        wii, wjj, side = patching[(ii, jj, facing)]
                        wfacing = (side + 2) % 4
                        i_inc = 0 if wfacing % 2 == 0 else 2 - wfacing
                        j_inc = 0 if wfacing % 2 == 1 else 1 - wfacing
                        ip, jp = rotate(i, j, size, (wfacing - facing) % 4)
                        ip = ip - size * i_inc
                        jp = jp - size * j_inc
                        k, l = ip + i_inc, jp + j_inc
                        match grove[(wii, wjj)][k][l]:
                            case ".":
                                facing = wfacing
                                ii, jj = wii, wjj
                                i, j = k, l
                                remaining -= 1
                            case "#":
                                break
    return 1000 * (ii * size + i + 1) + 4 * (jj * size + j + 1) + facing

def calculate_part1(file: str, size: int):
    grove, instructions = parse(file, size)
    patching = patch(grove)
    return walk(grove, instructions, size, patching)

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 22, part 1: {}".format(calculate_part1(file, 50)))
    # print("Dec 22, part 2: {}".format(calculate_part2(file)))
