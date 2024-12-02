def report_safety(levels):
    sign = 0
    for i in range(0, len(levels) - 1):
        diff = levels[i + 1] - levels[i]
        if diff > 0 and sign >= 0 and diff <= 3:
            sign = 1
        elif diff < 0 and sign <= 0 and diff >= -3:
            sign = -1
        else:
            return False
    return True


def part1(file: str):
    safe = 0
    with open(file, "r") as f:
        for report in f.readlines():
            levels = [int(_) for _ in report.split()]
            safe += int(report_safety(levels))
    return safe


def iter_levels_tolerable(levels):
    yield levels
    for i in range(len(levels)):
        yield levels[:i] + levels[(i + 1) :]


def part2(file: str):
    safe = 0
    with open(file, "r") as f:
        for report in f.readlines():
            levels = [int(_) for _ in report.split()]
            for l in iter_levels_tolerable(levels):
                if report_safety(l):
                    safe += 1
                    break
    return safe


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
