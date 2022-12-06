import sys

def first_n_distinct(chars: str, n: int) -> int:
    for i in range(n, len(chars)):
            if len(set(chars[i-n:i])) == n:
                return i

def calculate_part1(file: str):
    with open(file, "r") as f:
        line = f.readline()
        return first_n_distinct(line, 4)

def calculate_part2(file: str):
    with open(file, "r") as f:
        line = f.readline()
        return first_n_distinct(line, 14)
    return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 6, part 1: {}".format(calculate_part1(file)))
    print("Dec 6, part 2: {}".format(calculate_part2(file)))
