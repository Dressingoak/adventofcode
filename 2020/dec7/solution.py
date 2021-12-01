import re

inputs = open("input.txt").read().strip().split("\n")

class Bag:

    outer_pattern = r'^(\w+\s\w+) bags contain (.+)\.$'
    content_pattern = r'^(\d+)\s(\w+\s\w+) bags*'

    def __init__(self, regulation: str):
        outer = re.match(self.outer_pattern, regulation)
        if outer:
            self.color = outer.group(1)
            self.content = dict()
            for content in outer.group(2).split(", "):
                inner = re.match(self.content_pattern, content)
                if inner:
                    self.content[inner.group(2)] = int(inner.group(1))
    
    def __repr__(self):
        return "Bag<{}, {}>".format(self.color, self.content)

    def can_contain(self, key: str) -> bool:
        return key in self.content

regulations = [Bag(_) for _ in inputs]
# regulations = [Bag(_) for _ in [
#     "light red bags contain 1 bright white bag, 2 muted yellow bags.",
#     "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
#     "bright white bags contain 1 shiny gold bag.",
#     "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
#     "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
#     "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
#     "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
#     "faded blue bags contain no other bags.",
#     "dotted black bags contain no other bags."
# ]]

possible_bags = set()
possible_bags_prev = set(["shiny gold"])
diff = possible_bags_prev.copy()

i = 1
while True:
    for bag in regulations:
        for inner in diff:
            if bag.can_contain(inner):
                possible_bags.add(bag.color)
    if len(possible_bags) == len(possible_bags_prev):
        break
    diff = possible_bags.difference(possible_bags_prev)
    possible_bags_prev = possible_bags.copy()
    print("[DEBUG] Iteration {} complete ({} bags so far).".format(i, len(possible_bags)))
    i += 1

print("Part 1: {}".format(len(possible_bags)))

regulation_dict = {_.color: _ for _ in regulations}

def count_bags(key: str, count_self = False):
    bag = regulation_dict[key]
    return sum(num * count_bags(color, True) for (color, num) in bag.content.items()) + (1 if count_self else 0)

print("Part 2: {}".format(count_bags("shiny gold")))
