import sys
import re
sys.path.append('../')
from path_finding import dijkstra

def parse(file: str):
    pattern_id = re.compile(r"Blueprint (\d+)")
    pattern_costs = re.compile(r"Each (\w+) robot costs (\d+) (\w+)( and (\d+) (\w+))?\.")
    with open(file, "r") as f:
        for line in f.readlines():
            m = re.match(pattern_id, line)
            id = int(m.group(1))
            blueprint = {}
            for m in re.finditer(pattern_costs, line):
                match m.groups():
                    case (robot_type, count, resource, None, None, None):
                        blueprint[robot_type] = {resource: int(count)}
                    case (robot_type, count1, resource1, _, count2, resource2):
                        blueprint[robot_type] = {resource1: int(count1), resource2: int(count2)}
            yield id, blueprint

def can_proceed(check: str, robots: dict[str, int], allow: dict[str, int], blueprint: dict[str, dict[str, int]]):
    if robots[check] > 0:
        return True
    else:
        return all(can_proceed(robot, robots, allow, blueprint) and allow[check] for robot in blueprint[check].keys())

def get_next_states(state: tuple[int, int, int, int, int, int, int, int, int, bool, bool, bool, bool], blueprint: dict[str, dict[str, int]]):
    match state:
        case (time_remaining, ore, clay, obsidian, geode, n_ore, n_clay, n_obsidian, n_geode, a_ore, a_clay, a_obsidian, a_geode) if time_remaining > 0:
            robots = {"ore": ore, "clay": clay, "obsidian": obsidian, "geode": geode}
            resources = {"ore": n_ore, "clay": n_clay, "obsidian": n_obsidian, "geode": n_geode}
            allow = {"ore": a_ore, "clay": a_clay, "obsidian": a_obsidian, "geode": a_geode}
            if can_proceed("geode", robots, allow, blueprint):
                can_build = []
                if time_remaining > 1: # Check what robots can be built
                    for robot, requirements in blueprint.items():
                        if min(resources[material] // amount for material, amount in requirements.items()) > 0 and allow[robot]:
                            can_build.append(robot)
                for robot, amount in robots.items(): # Increase resources from current robots
                    resources[robot] += amount
                for robot in can_build + [None, ]:
                    next_robots = {r: a for r, a in robots.items()}
                    next_resources = {r: a for r, a in resources.items()}

                    if robot is None:
                        next_allow = {r: False if r in can_build else a for r, a in allow.items()}
                    else:
                        next_allow = {r: True for r in allow.keys()}
                        next_robots[robot] += 1
                        for material, amount in blueprint[robot].items():
                            next_resources[material] -= amount
                    next_state = (
                        time_remaining - 1, 
                        next_robots["ore"], next_robots["clay"], next_robots["obsidian"], next_robots["geode"],
                        next_resources["ore"], next_resources["clay"], next_resources["obsidian"], next_resources["geode"],
                        next_allow["ore"], next_allow["clay"], next_allow["obsidian"], next_allow["geode"]
                    )
                    yield next_state, robots["geode"]
    
def build_states(graph, state, blueprint):
    paths, explore = {}, []
    for next, geodes in get_next_states(state, blueprint):
        paths[next] = -geodes
        if next in graph:
            continue
        else:
            explore.append(next)
    graph[state] = paths
    for next in explore:
        build_states(graph, next, blueprint)
    return True

def calculate_part1(file: str):
    quality_level_sum = 0
    for id, blueprint in parse(file):
        start = (24, 1, 0, 0, 0, 0, 0, 0, 0, True, True, True, True)
        graph = {}
        build_states(graph, start, blueprint)
        _, states = dijkstra(graph, start, None)
        geodes = max(-value for value in states.values())
        print(f"[Finished simulation for blueprint {id} ({geodes} geodes, {len(graph)} states simulated)]")
        quality_level_sum += id * max(-value for value in states.values())
    return quality_level_sum

def calculate_part2(file: str):
    geodes = 1
    for id, blueprint in parse(file):
        if id > 3:
            break
        start = (32, 1, 0, 0, 0, 0, 0, 0, 0, True, True, True, True)
        graph = {}
        build_states(graph, start, blueprint)
        _, states = dijkstra(graph, start, None)
        geodes *= max(-value for value in states.values())
        print(f"[Finished simulation for blueprint {id} ({geodes} geodes, {len(graph)} states simulated)]")
    return geodes

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 19, part 1: {}".format(calculate_part1(file)))
    print("Dec 19, part 2: {}".format(calculate_part2(file)))
