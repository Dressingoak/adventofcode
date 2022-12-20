import sys

def calculate_part1(file: str):
    orig = []
    numbers = {}
    with open(file, "r") as f:
        for line in f.readlines():
            x = int(line.strip())
            orig.append(x)
            numbers[x] = None
    n = len(orig)
    for i, x in enumerate(orig):
        numbers[x] = [orig[(i-1) % n], orig[(i+1) % n]]
    print(numbers)
    for x in orig:
        if x == 0:
            continue
        steps, dir = abs(x) % n, 0 if x < 0 else 1
        y = x
        for _ in range(steps):
            y = numbers[y][dir]
        
        x_prev, x_next = numbers[x]
        y_prev, y_next = numbers[y]
        match dir:
            case 0:
                numbers[numbers[x][0]][1] = numbers[x][1]
                numbers[x][(dir + 1) % 2], numbers[x][dir] = y, numbers[y][dir]
                numbers[x]
                numbers[x_prev], numbers[x_next] = (numbers[x_prev][0], x_next), (x_prev, numbers[x_next][1])
                numbers[y_prev], numbers[y_next] = (numbers[x_prev][0], x_next), (x_prev, numbers[x_next][1])
        print(cur)
        break

    return 0

# def calculate_part2(file: str):
#     with open(file, "r") as f:
#         pass
#     return 0
    
if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 20, part 1: {}".format(calculate_part1(file)))
    # print("Dec 20, part 2: {}".format(calculate_part2(file)))
