def part1(file: str):
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

    return sum


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
