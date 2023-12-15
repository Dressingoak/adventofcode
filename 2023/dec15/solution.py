def HASH(seq: str) -> int:
    current_value = 0
    for char in seq:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            for seq in line.strip().split(","):
                sum += HASH(seq)
    return sum


def part2(file: str):
    sum = 0
    boxes = {}
    with open(file, "r") as f:
        for line in f.readlines():
            for seq in line.strip().split(","):
                if seq.endswith("-"):
                    label = seq[:-1]
                    h = HASH(label)
                    if h in boxes:
                        boxes[h]
                        i = -1
                        for j, (item, _) in enumerate(boxes[h]):
                            if label == item:
                                i = j
                                break
                        if i != -1:
                            boxes[h].pop(i)
                        if len(boxes[h]) == 0:
                            del boxes[h]
                else:
                    label, value = seq.split("=")
                    value = int(value)
                    h = HASH(label)
                    if h not in boxes:
                        boxes[h] = [(label, value)]
                    else:
                        i = -1
                        for j, (item, _) in enumerate(boxes[h]):
                            if label == item:
                                i = j
                                break
                        if i != -1:
                            boxes[h][i] = (label, value)
                        else:
                            boxes[h].append((label, value))
    sum = 0
    for box, lists in boxes.items():
        v1 = box + 1
        for i, (_, v3) in enumerate(lists):
            v2 = i + 1
            sum += v1 * v2 * v3
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
