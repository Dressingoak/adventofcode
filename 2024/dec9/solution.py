def pretty_print(files):
    s = ""
    for _, i, nxt in iter_files(files, 0):
        digit, size, free, _, nxt = files[i]
        for _ in range(free):
            s += "."
        # s += "[" + "|".join(str(digit) for _ in range(size)) + "]"
        s += "".join(str(digit) for _ in range(size))
        if nxt is not None:
            i = nxt
        else:
            break
    return s


def iter_files(files, start):
    i = start
    while True:
        yield files[i][-2], i, files[i][-1]
        if files[i][-1] is None:
            break
        else:
            i = files[i][-1]


def parse(file: str):
    files = []  # linked list
    with open(file, "r") as f:
        free = 0
        for pos, size in enumerate(f.readline().strip()):
            size = int(size)
            if pos % 2 == 0:
                i = pos // 2  # will eventually point to the last file
                files.append(
                    [
                        i,  # ID number
                        size,  # size
                        free,  # free space before
                        i - 1,  # previous block
                        i + 1,  # next block
                    ]
                )
            else:
                free = size
    files[0][-2] = None
    files[-1][-1] = None
    return files


def checksum(files):
    checksum = 0
    offset = 0
    for _, k, _ in iter_files(files, 0):
        for i in range(offset + files[k][2], offset + files[k][2] + files[k][1]):
            checksum += i * files[k][0]
        offset += files[k][1] + files[k][2]
    return checksum


def part1(file: str):
    files = parse(file)
    i = len(files) - 1
    k = 0
    completed = False
    while not completed:
        _, _, free, prv, nxt = files[k]
        if nxt is None:
            completed = True
            files[k][2] = 0
            break
        if free == 0:
            k = nxt
            continue
        if files[i][1] <= free:
            _i = files[i][-2]

            # Update the new end
            files[files[i][-2]][-1] = None

            # Move last file to the free space
            files[prv][-1] = i
            files[i][-2] = prv
            files[i][-1] = k
            files[k][-2] = i

            # Adjust free space
            files[k][2] -= files[i][1]
            files[i][2] = 0
            i = _i
        else:
            # Break up file
            files.append([files[i][0], free, 0, prv, k])
            j = len(files) - 1
            files[k][-2] = j
            files[k][2] = 0
            files[i][1] -= free
            files[prv][-1] = j

    return checksum(files)


def part2(file: str):
    files = parse(file)
    i = len(files) - 1
    while True:
        _, size, free, prv, nxt = files[i]
        if prv is None:
            break
        for k_prv, k, _ in iter_files(files, 1):
            if k == i:
                if size <= free:
                    # Move file as close to the left one as possible
                    files[i][2] = 0
                break
            if size <= files[k][2]:
                # Update the moved block's surroundings
                files[prv][-1] = nxt
                if nxt is not None:
                    files[nxt][-2] = prv
                    files[nxt][2] += size + free

                # Move last file to the free space
                files[k_prv][-1] = i
                files[i][-2] = k_prv
                files[i][-1] = k
                files[k][-2] = i

                # Adjust free space
                files[k][2] -= size
                files[i][2] = 0
                break
        i -= 1

    return checksum(files)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
