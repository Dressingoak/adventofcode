def part1(file: str):
    safe = 0
    with open(file, "r") as f:
        for report in f.readlines():
            levels = [int(_) for _ in report.split()]
            sign = 0
            invalid = False
            for i in range(0, len(levels) - 1):
                diff = levels[i+1] - levels[i]
                if diff > 0 and sign >= 0 and diff <= 3:
                    sign = 1
                elif diff < 0 and sign <= 0 and diff >= -3:
                    sign = -1
                else:
                    invalid = True
                    break
            if not invalid:
                safe += 1
    return safe


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
