import sys

def priority(char: str) -> int:
    ascii = ord(char)
    if ascii >= 97 and ascii <= 122:
        return ascii - 96 # a..z => 1..27
    elif ascii >= 65 and ascii <= 90:
        return ascii - 38 # A..Z => 27..52

def get_common(arrangement: str) -> str:
    n = len(arrangement)
    m = n // 2
    l, r = set(arrangement[0:m]), set(arrangement[m:n])
    match [_ for _ in l.intersection(r)]:
        case [x]: return x
        case _: raise Exception("Not exactly one common item!")

print(get_common("ttgJtRGJQctTZtZT"))

def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            arrangement = line.strip()
            if arrangement == "":
                continue
            c = get_common(arrangement)
            s += priority(c)
    return s

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 3, part 1: {}".format(calculate_part1(file)))
    # print("Dec 3, part 2: {}".format(calculate_part2(file)))
