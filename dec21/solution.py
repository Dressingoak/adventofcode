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

ingredients = set()
allergens = set()
for food in data:
    ingredients.update(set(food[0]))
    allergens.update(set(food[1]))
print("[DEBUG] All ingredients: {}".format(sorted(list(ingredients))))
print("[DEBUG] All allergens: {}".format(sorted(list(allergens))))

def solution_exist(foods: list[tuple[list[str], list[str]]], test: tuple[str, str], blacklist: list[tuple[str, str]] = list(), depth = 0):
    (i, a) = test
    new_foods = []
    for (ingredients, allergens) in foods:
        if a in allergens and i not in ingredients:
            return False
        else:
            new_foods.append(
                ([_ for _ in ingredients if _ != i], [_ for _ in allergens if _ != a])
            )
    ingredients = set()
    allergens = set()
    for (i, a) in new_foods: 
        ingredients.update(set(i))
        allergens.update(set(a))
    if len(allergens) == 0:
        return True
    print("[DEBUG] At depth {}, {} ingredients and {} allergens remaining".format(depth, len(ingredients), len(allergens)))
    skip = []
    for (i, a) in itertools.product(ingredients, allergens):
        if (i, a) in blacklist:
            continue
        res = solution_exist(new_foods, (i, a), skip, depth+1)
        if res:
            return True
        else:
            skip.append((i, a))
    return False

def safe_ingredients(foods):
    ingredients = set()
    allergens = set()
    for food in foods:
        ingredients.update(set(food[0]))
        allergens.update(set(food[1]))
    unsafe = set()
    for i in ingredients:
        print("[DEBUG] Checking ingredient '{}'".format(i))
        for a in allergens:
            if solution_exist(data, (i, a)):
                unsafe.add(i)
                break
    return ingredients.difference(unsafe)

safe = safe_ingredients(data)
print("[DEBUG] Safe ingredients are: {}".format(safe))
