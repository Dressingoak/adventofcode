def parse_and_sum(file: str, correct: bool):
    sum = 0
    parse_orderings = True
    page_orders = {}
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                parse_orderings = False
                continue
            if parse_orderings:
                page, before = line.split("|")
                page, before = int(page), int(before)
                if page in page_orders:
                    page_orders[page].add(before)
                else:
                    page_orders[page] = set([before])
            else:
                pages = [int(_) for _ in line.split(",")]
                n = len(pages)
                if not correct:
                    acceptable = True
                    for i, page in enumerate(pages):
                        if not all(
                            page in page_orders and p in page_orders[page]
                            for p in pages[i + 1 :]
                        ):
                            acceptable = False
                            break
                    if acceptable:
                        sum += pages[len(pages) // 2]
                else:
                    acceptable = False
                    corrected = False
                    while not acceptable:
                        for i in range(n - 1):
                            a, b = pages[i], pages[i + 1]
                            if a in page_orders and b in page_orders[a]:
                                if i + 2 == n:
                                    acceptable = True
                            else:
                                pages[i + 1], pages[i] = pages[i], pages[i + 1]
                                corrected = True
                                break
                    if corrected:
                        sum += pages[len(pages) // 2]
    return sum


def part1(file: str):
    return parse_and_sum(file, False)


def part2(file: str):
    return parse_and_sum(file, True)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
