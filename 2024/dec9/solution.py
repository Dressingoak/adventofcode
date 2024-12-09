def pretty_print(files):
    s = ""
    for _, i, nxt in iter_files(files, 0):
        digit, size, free, _, nxt = files[i]
        for _ in range(free):
            s += "."
        s += "["
        for _ in range(size):
            s += f"{digit}"
        s += "]"
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


def part1(file: str):
    checksum = 0
    files = []  # linked list
    with open(file, "r") as f:
        free = 0
        for pos, size in enumerate(f.readline().strip()):
            size = int(size)
            if pos % 2 == 0:
                i = pos // 2  # will eventually point to the last file
                files.append([i, size, free, i - 1, i + 1])
            else:
                free = size
    files[0][-2] = None
    files[-1][-1] = None

    k = 0
    completed = False
    while not completed:
        _, size, free, prv, nxt = files[k]
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

    offset = 0
    for _, k, _ in iter_files(files, 0):
        for i in range(offset, offset + files[k][1]):
            # print(i, files[k][0])
            checksum += i * files[k][0]
        offset += files[k][1]

    return checksum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
