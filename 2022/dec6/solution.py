import sys

def calculate_part1(file: str):
    with open(file, "r") as f:
        line = f.readline()
        for i in range(4, len(line)):
            if len(set(line[i-4:i])) == 4:
                return i

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 6, part 1: {}".format(calculate_part1(file)))
    # print("Dec 6, part 2: {}".format(calculate_part2(file)))
