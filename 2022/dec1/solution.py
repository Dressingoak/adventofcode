import sys

def calculate_part1(file: str):
    cur, max = 0, 0
    with open(file, "r") as f:
        for line in f.readlines():
            match line.strip():
                case "":
                    if cur > max:
                        max = cur
                    cur = 0
                case x:
                    cur += int(x)
        if cur > max:
            max = cur
    return max

def calculate_part2(file: str):
    cur, l = 0, []
    with open(file, "r") as f:
        for line in f.readlines():
            match line.strip():
                case "":
                    l.append(cur)
                    cur = 0
                case x:
                    cur += int(x)
        if cur > 0:
            l.append(cur)
    l.sort(reverse=True)
    return sum(l[:3])

    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 1, part 1: {}".format(calculate_part1(file)))
    print("Dec 1, part 2: {}".format(calculate_part2(file)))
