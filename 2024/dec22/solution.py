def mix(n, s):
    return n ^ s


def prune(s):
    return s % 16777216


def draw(n, step=0):
    yield n
    while True:
        match step:
            case 0:
                n = prune(mix(n * 64, n))
                step += 1
            case 1:
                n = prune(mix(n // 32, n))
                step += 1
            case 2:
                n = prune(mix(n * 2048, n))
                step = 0
        if step == 0:
            yield n


def part1(file: str):
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            n = int(line.strip())
            for i, s in enumerate(draw(n)):
                if i == 2000:
                    print(f"{n}: {s}")
                    sum += s
                    break
    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
