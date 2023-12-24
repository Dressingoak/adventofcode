def det(a, b, c, d):
    return a * d - b * c


def part1(file: str, least=200000000000000, most=400000000000000):
    hailstorms = []
    with open(file) as f:
        for line in f:
            p, v = line.strip().split("@")
            hailstorms.append(
                ([int(_) for _ in p.split(", ")], [int(_) for _ in v.split(", ")])
            )
    count = 0
    for i, hs1 in enumerate(hailstorms):
        x1, y1 = hs1[0][:2]
        x2, y2 = x1 + hs1[1][0], y1 + hs1[1][1]
        for hs2 in hailstorms[i + 1 :]:
            x3, y3 = hs2[0][:2]
            x4, y4 = x3 + hs2[1][0], y3 + hs2[1][1]

            t = det(x1 - x3, x3 - x4, y1 - y3, y3 - y4)
            u = det(x1 - x3, x1 - x2, y1 - y3, y1 - y2)
            d = det(x1 - x2, x3 - x4, y1 - y2, y3 - y4)
            match d:
                case 0:
                    continue
                case _ if d > 0:
                    if t < 0 or u < 0:
                        continue
                    if least * d > x1 * d + t * (x2 - x1):
                        continue
                    if most * d < x1 * d + t * (x2 - x1):
                        continue
                    if least * d > y1 * d + t * (y2 - y1):
                        continue
                    if most * d < y1 * d + t * (y2 - y1):
                        continue
                case _:
                    if t > 0 or u > 0:
                        continue
                    if least * d < x1 * d + t * (x2 - x1):
                        continue
                    if most * d > x1 * d + t * (x2 - x1):
                        continue
                    if least * d < y1 * d + t * (y2 - y1):
                        continue
                    if most * d > y1 * d + t * (y2 - y1):
                        continue
            count += 1

    return count


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
