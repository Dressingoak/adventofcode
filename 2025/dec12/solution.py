def shape_str(shape):
    s = ""
    for r in shape:
        s += "".join("#" if c else "." for c in r) + "\n"
    return s.strip()


def rotate(shape):
    h, w = len(shape), len(shape[0])
    new = [[None for y in range(h)] for x in range(w)]
    for x in range(w):
        for y in range(h):
            x_t = h - 1 - y
            y_t = x
            new[y_t][x_t] = shape[y][x]
    return tuple(tuple(r) for r in new)


def flip(shape):
    return tuple(tuple(reversed(r)) for r in shape)


def iter_rotations_and_flips(shape):
    yield shape
    yield flip(shape)
    s = shape
    for _ in range(3):
        s = rotate(s)
        yield s
        yield flip(s)


def parse(file: str):
    with open(file, "r") as f:
        blocks = []
        buffer = ""
        for line in f.readlines():
            if (l := line.strip()) == "":
                blocks.append(buffer.strip())
                buffer = ""
            else:
                buffer += l + "\n"
    shapes = {}
    for b in blocks:
        idx, *rows = b.split()
        shape = tuple(tuple(c == "#" for c in l) for l in rows)
        shapes[int(idx[:-1])] = set(iter_rotations_and_flips(shape))
    regions = []
    for region in buffer[:-1].split("\n"):
        area, *amount = region.split()
        w, h = area[:-1].split("x")
        regions.append(((int(w), int(h)), [int(_) for _ in amount]))
    return shapes, regions


def part1(file: str):
    total = 0
    shapes, regions = parse(file)
    # for i, ss in shapes.items():
    #     print(i)
    #     rows = [shape_str(s).split() for s in ss]
    #     n = len(rows[0])
    #     for i in range(n):
    #         print("   ".join(rows[j][i] for j in range(len(rows))))
    #     print()
    sizes = {}
    for i, shape in shapes.items():
        s = next(_ for _ in shape)
        area = sum(sum(int(c) for c in l) for l in s)
        sizes[i] = area
        # print(f"size({i=}): {area}")
    shape_coords = {}
    for k, ss in shapes.items():
        shape_coords[k] = []
        for s in ss:
            I = set()
            for i, r in enumerate(s):
                for j, c in enumerate(r):
                    if c:
                        I.add((i, j))
            shape_coords[k].append(I)
        # print(k, shape_coords[k])
    for (w, h), amount in regions:
        cap = w * h
        to_fit = sum(sizes[i] * n for i, n in enumerate(amount))
        free = max(0, cap - to_fit)
        if free == 0:
            continue
        # print(f"Free: {free:4.0f} ({free / cap * 100:4.1f}%), to fit: {amount}")

        # Try fit in the shapes
        indices = [[(i, j) for j in range(w)] for i in range(h)]
        indices_set = set(idx for rows in indices for idx in rows)

        filled = set()
        fitted = [0 for _ in range(len(amount))]

        def fit_shape(shape_idx):
            if shape_idx == len(amount):
                return True
            if amount[shape_idx] == fitted[shape_idx]:
                return fit_shape(shape_idx + 1)
            for k, l in sorted(indices_set - filled):
                for coords in shape_coords[shape_idx]:
                    option = set((k + i, l + j) for i, j in coords)
                    if any((i >= h) or (j >= w) for i, j in option):
                        continue
                    if filled.isdisjoint(option):
                        fitted[shape_idx] += 1
                        filled.update(option)
                        if fit_shape(shape_idx):
                            return True
                        else:
                            fitted[shape_idx] -= 1
                            filled.difference_update(option)
            return False

        res = fit_shape(0)
        # if res:
        #     mat = [["." for x in range(w)] for y in range(h)]
        #     for ii, jj in filled:
        #         mat[ii][jj] = "#"
        #     print("\n".join("".join(mat[ii]) for ii in range(len(mat))).strip())
        total += int(res)
    return total


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
