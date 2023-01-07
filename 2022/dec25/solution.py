import sys
sys.path.append('../')
from timing import print_timing

def snafu_to_decimal(x):
    lst = []
    for char in x:
        match char:
            case "0" | "1" | "2": lst.append(int(char))
            case "-": lst.append(-1)
            case "=": lst.append(-2)
    return sum(5**i * v for i, v in enumerate(reversed(lst)))

def gen_decimal_to_snafu(x):
    if x > 0:
        shifted = (x+2) % 5
        match shifted:
            case 0: yield "="
            case 1: yield "-"
            case 2: yield "0"
            case 3: yield "1"
            case 4: yield "2"
        yield from gen_decimal_to_snafu((x+2-shifted) // 5)

def decimal_to_snafu(x):
    return "".join(reversed([_ for _ in gen_decimal_to_snafu(x)]))

@print_timing
def calculate_part1(file: str):

    s = 0
    with open(file, "r") as f:
        for line in f.readlines():
            s += snafu_to_decimal(line.rstrip())
    return decimal_to_snafu(s)

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 25, part 1: {} (took {})".format(*calculate_part1(file)))
