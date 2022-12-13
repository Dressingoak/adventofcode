import sys

def parse_packet(packet: str):
    i, l = 1, []
    num = ""
    while i < len(packet):
        if packet[i] == "[":
            c, j = 1, i
            while c > 0:
                i+=1
                if packet[i] == "[":
                    c+=1
                elif packet[i] == "]":
                    c-=1
            l.append(parse_packet(packet[j:(i+1)]))
            i+=1
        elif packet[i] == "]":
            if len(num) > 0:
                l.append(int(num))
            return l
        elif packet[i] == ",":
            if len(num) > 0:
                l.append(int(num))
            num = ""
            i+=1
        else:
            num += packet[i]
            i+=1

def parse_packets(file: str):
    pairs = []
    with open(file, "r") as f:
        pair = []
        for i, line in enumerate(f.readlines()):
            if (i+1) % 3 == 0:
                pairs.append((pair[0], pair[1]))
                pair = []
                pass
            else:
                pair.append(parse_packet(line.strip()))
        pairs.append((pair[0], pair[1]))
    return pairs

def compare(left, right):
    for i in range(min(len(left), len(right))):
        match (left[i], right[i]):
            case (a, b) if isinstance(a, int) and isinstance(b, int):
                a, b = int(a), int(b)
                if a < b:
                    return True
                elif a > b:
                    return False
            case (a, b) if isinstance(a, list) and isinstance(b, list):
                res = compare(a, b)
                if res is not None:
                    return res
            case (a, b) if isinstance(a, int) and isinstance(b, list):
                res = compare([a], b)
                if res is not None:
                    return res
            case (a, b) if isinstance(a, list) and isinstance(b, int):
                res = compare(a, [b])
                if res is not None:
                    return res
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False

def calculate_part1(file: str):
    packets = parse_packets(file)
    s = 0
    for i, (left, right) in enumerate(packets):
        if compare(left, right):
            s += i+1
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

    print("Dec 13, part 1: {}".format(calculate_part1(file)))
    # print("Dec 13, part 2: {}".format(calculate_part2(file)))
