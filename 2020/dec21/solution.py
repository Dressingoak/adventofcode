import re
import itertools

pattern = re.compile(r'^(?P<ingredients>[\w\s]*\w)\s\(contains\s(?P<allergens>[\w\,\s]*\w)+\)$')

data = []
for line in open("input.txt").read().strip().split("\n"):
    m = pattern.match(line)
    if m:
        raw = m.groupdict()
        data.append((raw["ingredients"].split(" "), raw["allergens"].split(", ")))
    else:
        raise Exception("Could not match line: '{}'".format(line))

def is_solution(foods: list[tuple[list[str], list[str]]], pairs: list[tuple[str, str]], max_depth: int = None, depth: int = 0):
    (i, a) = pairs[0]
    new_foods = []
    for (ingredients, allergens) in foods:
        if a in allergens and i not in ingredients:
            return False
        else:
            new_foods.append(
                ([_ for _ in ingredients if _ != i], [_ for _ in allergens if _ != a])
            )
    allergens = set()
    for (_, a) in new_foods: 
        allergens.update(set(a))
    if len(allergens) == 0:
        return True
    else:
        if max_depth is not None and depth + 1 == max_depth:
            return None
        else:
            return is_solution(new_foods, pairs[1:], max_depth, depth+1)

def ingredient_allergen_combinations(food_dict, current=[], target_size=None):
    if target_size is not None and len(current) == target_size:
        return {k: v for (k,v) in current}
    if target_size is None:
        allergens = set()
        for algs in food_dict.values():
            allergens.update(set(algs))
        target_size = len(allergens)
    explored = []
    for i, algs in food_dict.items():
        explored.append(i)
        for a in algs:
            new_food_dict = {k: [_ for _ in v if _ != a] for (k,v) in food_dict.items() if k not in explored}
            x = yield from ingredient_allergen_combinations(new_food_dict, current + [(i, a)], target_size)
            if x is not None:
                yield x

def unsafe_ingredients(foods, food_dict):
    ingredients = set()
    allergens = set()
    for i, a in food_dict.items():
        ingredients.add(i)
        allergens.update(set(a))
    unsafe = set()
    solutions = set()
    for pairs in ingredient_allergen_combinations(food_dict):
        print("[DEBUG] Checking possible solution {}".format(pairs))
        if is_solution(foods, [(k,v) for (k,v) in pairs.items()]):
            print("[DEBUG] - That is a solution!")
            unsafe.update(set(_ for _ in pairs.keys()))
            solutions.add(tuple(sorted([(k,v) for (k,v) in pairs.items()], key=lambda x: x[1])))
    return (unsafe, solutions)

def safe_ingredients(foods):
    ingredients = set()
    allergens = set()
    for food in foods:
        ingredients.update(set(food[0]))
        allergens.update(set(food[1]))
    food_dict = dict()
    for i in ingredients:
        possible = set()
        for a in allergens:
            pairs = [(i, a)]
            res = is_solution(foods, pairs, 1)
            if res != False:
                possible.add(a)
                print("[DEBUG] '{}' could contain '{}'".format(i, a))
        if len(possible) > 0:
            food_dict[i] = possible
    (unsafe, solutions) = unsafe_ingredients(foods, food_dict)
    return ingredients.difference(unsafe), solutions

(safe, solutions) = safe_ingredients(data)
print("[DEBUG] Safe ingredients are: {}".format(safe))
print("[DEBUG] Possible solutions are:")
for s in solutions:
    print("[DEBUG] - {}".format(s))

appearances = sum(sum(1 if i in safe else 0 for i in ingredients) for (ingredients, _) in data)
print("Part 1: {}".format(appearances))
solution = next(iter(solutions))
print("Part 2: '{}'".format(",".join([i for (i,_) in solution])))
