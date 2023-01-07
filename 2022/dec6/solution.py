import sys
sys.path.append('../')
from timing import print_timing

def first_n_distinct(chars: str, n: int) -> int:
    for i in range(n, len(chars)):
            if len(set(chars[i-n:i])) == n:
                return i

@print_timing
def calculate_part1(file: str):
    with open(file, "r") as f:
        line = f.readline()
        return first_n_distinct(line, 4)

@print_timing
def calculate_part2(file: str):
    with open(file, "r") as f:
        line = f.readline()
        return first_n_distinct(line, 14)
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 6, part 1: {} (took {})".format(*calculate_part1(file)))
    print("Dec 6, part 2: {} (took {})".format(*calculate_part2(file)))
