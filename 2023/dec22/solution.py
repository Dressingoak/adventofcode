def parse_bricks(file: str):
    bricks = []
    with open(file) as f:
        for line in f:
            brick = set()
            ends = line.strip().split("~")
            x1, y1, z1 = (int(_) for _ in ends[0].split(","))
            x2, y2, z2 = (int(_) for _ in ends[1].split(","))
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    for z in range(z1, z2 + 1):
                        brick.add((x, y, z))
            bricks.append(brick)
    return bricks


def place_bricks(bricks):
    bricks_fallen = []
    height_map = {}
    for brick in bricks:
        top_view = set((x, y) for x, y, _ in brick)
        z_min, z_max = min(z for _, _, z in brick), max(z for _, _, z in brick)
        intersection = {k: h for k, h in height_map.items() if k in top_view}
        offset = 1
        if len(intersection) > 0:
            offset += max(_ for _ in intersection.values())
        height_map.update({xy: z_max - z_min + offset for xy in top_view})
        brick_fallen = set()
        for x, y in top_view:
            for z in range(offset, offset + (z_max - z_min) + 1):
                brick_fallen.add((x, y, z))
        bricks_fallen.append(brick_fallen)
    return bricks_fallen


def part1(file: str):
    bricks = parse_bricks(file)
    bricks.sort(key=lambda cube: min(z for _, _, z in cube))
    bricks_fallen = place_bricks(bricks)
    count = 0
    for i in range(len(bricks_fallen)):
        wo = [b for j, b in enumerate(bricks_fallen) if i != j]
        wop = place_bricks(wo)
        if all(l == r for l, r in zip(wo, wop)):
            count += 1
    return count


def part2(file: str):
    bricks = parse_bricks(file)
    bricks.sort(key=lambda cube: min(z for _, _, z in cube))
    bricks_fallen = place_bricks(bricks)
    count = 0
    for i in range(len(bricks_fallen)):
        wo = [b for j, b in enumerate(bricks_fallen) if i != j]
        wop = place_bricks(wo)
        count += sum(1 for l, r in zip(wo, wop) if l != r)
    return count


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
