import sys
import re
sys.path.append('../')
from path_finding import a_star

def ceildiv(a, b):
    return -(a // -b)

class RobotFactory:
    pattern_id = re.compile(r"Blueprint (\d+)")
    pattern_costs = re.compile(r"Each (\w+) robot costs (\d+) (\w+)( and (\d+) (\w+))?\.")

    def __init__(self, id: int, blueprint: dict[str, dict[str, int]]):
        self.id = id
        self.blueprint = blueprint
        self.limits = {material: max((requirements[material] for requirements in self.blueprint.values() if material in requirements), default=0) for material in ["ore", "clay", "obsidian"]}

    def __repr__(self) -> str:
        return f"Blueprint {self.id}: {self.blueprint}"

    def parse(string: str):
        m = re.match(RobotFactory.pattern_id, string)
        id = int(m.group(1))
        blueprint = {}
        for m in re.finditer(RobotFactory.pattern_costs, string):
            match m.groups():
                case (robot_type, count, resource, None, None, None):
                    blueprint[robot_type] = {resource: int(count)}
                case (robot_type, count1, resource1, _, count2, resource2):
                    blueprint[robot_type] = {resource1: int(count1), resource2: int(count2)}
        return RobotFactory(id, blueprint)

    def get_next_states(self, state: tuple[int, int, int, int, int, int, int]):
        match state:
            case (time_remaining, bots_ore, bots_clay, bots_obsidian, amount_ore, amount_clay, amount_obsidian) if time_remaining > 1:
                rates = {"ore": bots_ore, "clay": bots_clay, "obsidian": bots_obsidian}
                resources = {"ore": amount_ore, "clay": amount_clay, "obsidian": amount_obsidian}
                for robot, requirements in self.blueprint.items():
                    if robot in self.limits and rates[robot] >= self.limits[robot]:
                        continue
                    if any(rates[material] == 0 for material, amount in requirements.items() if amount > 0): # Materials needed are not produced
                        continue
                    required_time = 0
                    next_resources = {r: a for r, a in resources.items()}
                    for material, amount in requirements.items():
                        needed = amount - resources[material]
                        time = ceildiv(needed, rates[material]) if needed > 0 else 0 # Solves for time: time * rate >= resources needed
                        required_time = max(required_time, time)
                        next_resources[material] -= amount
                    if time_remaining - required_time - 1 > 0:
                        next_rates = {r: a + (1 if r == robot else 0) for r, a in rates.items()}
                        for r in resources.keys():
                            next_resources[r] += (required_time + 1) * rates[r]
                        next_state = (
                            time_remaining - required_time - 1, 
                            next_rates["ore"], next_rates["clay"], next_rates["obsidian"],
                            next_resources["ore"], next_resources["clay"], next_resources["obsidian"]
                        )
                        yield next_state, 0 if robot != "geode" else (time_remaining - required_time - 1)
    
    def gen_states(self, state: tuple[int, int, int, int, int, int, int]):
        following = [_ for _ in self.get_next_states(state)]
        if len(following) == 0:
            yield (0, 0, 0, 0, 0, 0, 0), 0
        else:
            for (next, cost) in following:
                yield next, -cost


    def estimate(self, state: tuple[int, int, int, int, int, int, int]):
        time_remaining = state[0]
        return - time_remaining * (time_remaining - 1) // 2 # sum(-i, i=1..time_remaining)

    def get_maximal_geodes(self, time):
        start = (time, 1, 0, 0, 0, 0, 0)
        end = (0, 0, 0, 0, 0, 0, 0)
        _, cost = a_star(self.gen_states, start, end, self.estimate)
        return cost

def calculate_part1(file: str):
    quality_level_sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            factory = RobotFactory.parse(line.rstrip())
            geodes = -factory.get_maximal_geodes(24)
            print(f"[Finished simulating for blueprint {factory.id} ({geodes} geodes)]")
            quality_level_sum += factory.id * geodes
    return quality_level_sum

def calculate_part2(file: str):
    geodes_prod = 1
    with open(file, "r") as f:
        for line in f.readlines():
            factory = RobotFactory.parse(line.rstrip())
            if factory.id > 3:
                continue
            geodes = -factory.get_maximal_geodes(32)
            print(f"[Finished simulating for blueprint {factory.id} ({geodes} geodes)]")
            geodes_prod *= geodes
    return geodes_prod

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 19, part 1: {}".format(calculate_part1(file)))
    print("Dec 19, part 2: {}".format(calculate_part2(file)))
