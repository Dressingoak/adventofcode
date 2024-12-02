def report_safety(levels):
    diffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
    return all(d >= 1 and d <= 3 for d in diffs) or all(
        d <= -1 and d >= -3 for d in diffs
    )


def part1(file: str):
    safe = 0
    with open(file, "r") as f:
        for report in f.readlines():
            levels = [int(_) for _ in report.split()]
            safe += int(report_safety(levels))
    return safe


def iter_levels_tolerable(levels):
    yield (-1, levels)
    for i in range(len(levels)):
        yield (i, levels[:i] + levels[(i + 1) :])


def part2(file: str):
    safe = 0
    with open(file, "r") as f:
        for report in f.readlines():
            levels = [int(_) for _ in report.split()]
            for i, l in iter_levels_tolerable(levels):
                if report_safety(l):
                    safe += 1
                    break
    return safe


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
