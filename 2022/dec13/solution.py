import sys
sys.path.append('../')
from puzzle import Puzzle

def parse_packet(packet: str) -> list:
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

def parse_packets(file: str) -> list[tuple[list, list]]:
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

def sorter(lst: list, gt) -> list:
    n = len(lst)
    for i in range(n):
        is_sorted = True
        for j in range(n - i - 1):
            if gt(lst[j], lst[j+1]):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                is_sorted = False
        if is_sorted:
            break

def calculate_part1(file: str):
    packets = parse_packets(file)
    return sum(i+1 for i, (left, right) in enumerate(packets) if compare(left, right))

def calculate_part2(file: str):
    packets = parse_packets(file)
    decoders: set[list] = [[[2]], [[6]]]
    all_packets = [_ for _ in decoders]
    for pair in packets:
        match pair:
            case (l, r): all_packets.extend([l, r])
    sorter(all_packets, lambda x, y: compare(y, x))
    p = 1
    for i, packet in enumerate(all_packets):
        if any(compare(packet, decoder) is None for decoder in decoders):
            p *= i+1
    return p
    
if __name__ == '__main__':

    puzzle = Puzzle(__file__)

    puzzle.add_part(1, calculate_part1)
    puzzle.add_part(2, calculate_part2)

    puzzle.run()
