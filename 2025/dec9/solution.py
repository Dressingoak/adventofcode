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


def shoelace(points):
    shoelace = 0
    for i in range(len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]
        shoelace += x1 * y2 - x2 * y1
    return shoelace // 2


def tiles_to_outline(points):
    """Generate the points making up the outline of tiles, i.e. determine the correct corners of the tiles for the path

    For example, `[(3, 3), (3, 4), (4, 4), (4, 3)]` is a negatively oriented polygon with outline `[(3, 3), (3, 5), (5, 5), (5, 3)]`.

    Determining corners requires us to find the winding of the path."""
    orientation = shoelace(points) > 0
    p = points if orientation else list(reversed(points))
    x0, y0 = p[-1]
    x1, y1 = p[0]
    x2, y2 = p[1]
    corners = []
    for i in range(len(p)):
        x0, y0 = p[i - 1]
        x1, y1 = p[i]
        x2, y2 = p[i + 1 if i + 1 < len(p) else 0]
        if x1 == x0:
            if y0 < y1:
                if x2 > x1:
                    dx, dy = 1, 0
                else:
                    dx, dy = 1, 1
            else:
                if x2 > x1:
                    dx, dy = 0, 0
                else:
                    dx, dy = 0, 1
        else:
            if x0 < x1:
                if y2 > y1:
                    dx, dy = 1, 0
                else:
                    dx, dy = 0, 0
            else:
                if y2 > y1:
                    dx, dy = 1, 1
                else:
                    dx, dy = 0, 1
        corners.append((x1 + dx, y1 + dy))
    return corners


def part2(file: str):
    tiles = []
    with open(file, "r") as f:
        for line in f.readlines():
            x, y = line.strip().split(",")
            tiles.append(
                (int(x), -int(y))
            )  # Mirror y to get correct orientations for the shape
    n = len(tiles)
    outline = tiles_to_outline(tiles)
    largest = 0
    for i in range(n):
        x1, y1 = tiles[i]
        for j in range(i + 1, n):
            x2, y2 = tiles[j]
            size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if size > largest:
                xl, xh = min(x1, x2), max(x1, x2) + 1
                yl, yh = min(y1, y2), max(y1, y2) + 1
                # Clamp the outline to the region of the rectangle
                # The area is always <= area of the rectangle since a lot of the swept out path have zero area
                clamped_outline = [
                    (max(min(x, xh), xl), max(min(y, yh), yl)) for (x, y) in outline
                ]
                if shoelace(clamped_outline) == size:
                    largest = size
    return largest


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
