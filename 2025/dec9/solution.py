def part1(file: str):
    tiles = []
    with open(file, "r") as f:
        for line in f.readlines():
            x, y = line.strip().split(",")
            tiles.append((int(x), int(y)))
    n = len(tiles)
    largest = 0
    for i in range(n):
        x1, y1 = tiles[i]
        for j in range(i + 1, n):
            x2, y2 = tiles[j]
            size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if size > largest:
                largest = size
    return largest


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
