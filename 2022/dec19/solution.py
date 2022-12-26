import sys
import re
sys.path.append('../')
from path_finding import dijkstra

class RobotFactory:
    pattern_id = re.compile(r"Blueprint (\d+)")
    pattern_costs = re.compile(r"Each (\w+) robot costs (\d+) (\w+)( and (\d+) (\w+))?\.")

    def __init__(self, id: int, blueprint: dict[str, dict[str, int]]):
        self.id = id
        self.blueprint = blueprint

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

    def can_proceed(self, check: str, robots: dict[str, int], allow: dict[str, int]):
        if robots[check] > 0:
            return True
        else:
            return all(self.can_proceed(robot, robots, allow) and allow[check] for robot in self.blueprint[check].keys())

    def get_next_states(self, state: tuple[int, int, int, int, int, int, int, int, int, bool, bool, bool, bool]):
        match state:
            case (time_remaining, ore, clay, obsidian, geode, n_ore, n_clay, n_obsidian, n_geode, a_ore, a_clay, a_obsidian, a_geode) if time_remaining > 0:
                robots = {"ore": ore, "clay": clay, "obsidian": obsidian, "geode": geode}
                resources = {"ore": n_ore, "clay": n_clay, "obsidian": n_obsidian, "geode": n_geode}
                allow = {"ore": a_ore, "clay": a_clay, "obsidian": a_obsidian, "geode": a_geode}
                if self.can_proceed("geode", robots, allow):
                    can_build = []
                    if time_remaining > 1: # Check what robots can be built
                        for robot, requirements in self.blueprint.items():
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
                            for material, amount in self.blueprint[robot].items():
                                next_resources[material] -= amount
                        next_state = (
                            time_remaining - 1, 
                            next_robots["ore"], next_robots["clay"], next_robots["obsidian"], next_robots["geode"],
                            next_resources["ore"], next_resources["clay"], next_resources["obsidian"], next_resources["geode"],
                            next_allow["ore"], next_allow["clay"], next_allow["obsidian"], next_allow["geode"]
                        )
                        yield next_state, robots["geode"]
        
    def build_states(self, graph, state):
        paths, explore = {}, []
        for next, geodes in self.get_next_states(state):
            paths[next] = -geodes
            if next in graph:
                continue
            else:
                explore.append(next)
        graph[state] = paths
        for next in explore:
            self.build_states(graph, next)
        return True

def calculate_part1(file: str):
    quality_level_sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            factory = RobotFactory.parse(line.rstrip())
            start = (20, 1, 0, 0, 0, 0, 0, 0, 0, True, True, True, True)
            graph = {}
            factory.build_states(graph, start)
            _, states = dijkstra(graph, start, None)
            geodes = max(-value for value in states.values())
            print(f"[Finished simulation for blueprint {factory.id} ({geodes} geodes, {len(graph)} states simulated)]")
            quality_level_sum += factory.id * max(-value for value in states.values())
    return quality_level_sum

def calculate_part2(file: str):
    geodes = 1
    with open(file, "r") as f:
        for line in f.readlines():
            factory = RobotFactory.parse(line.rstrip())
            if factory.id > 3:
                pass
            start = (20, 1, 0, 0, 0, 0, 0, 0, 0, True, True, True, True)
            graph = {}
            factory.build_states(graph, start)
            _, states = dijkstra(graph, start, None)
            geodes = max(-value for value in states.values())
            print(f"[Finished simulation for blueprint {factory.id} ({geodes} geodes, {len(graph)} states simulated)]")
            geodes *= max(-value for value in states.values())
    return geodes

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 19, part 1: {}".format(calculate_part1(file)))
    print("Dec 19, part 2: {}".format(calculate_part2(file)))
