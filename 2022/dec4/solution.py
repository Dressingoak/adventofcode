import sys

def to_range(lst: str) -> tuple[int, int]:
    l, r = lst.split("-")
    return (int(l), int(r))

def calculate_part1(file: str):
    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            e1, e2 = [to_range(_) for _ in line.strip().split(",")]
            if (e1[0] <= e2[0] and e1[1] >= e2[1]) or (e2[0] <= e1[0] and e2[1] >= e1[1]):
                s += 1
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

    print("Dec 4, part 1: {}".format(calculate_part1(file)))
    # print("Dec 4, part 2: {}".format(calculate_part2(file)))
