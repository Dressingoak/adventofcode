import sys
import re
sys.path.append('../')
from path_finding import dijkstra

def parse(file: str):
    pattern = re.compile(r"Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)")
    with open(file, "r") as f:
        for line in f.readlines():
            m = re.match(pattern, line.strip())
            valve, flow_rate, valves = m.group(1, 2, 3)
            yield valve, int(flow_rate), valves.split(", ")

def get_connection_costs(file: str, start_valve: str):
    connections = {}
    flow_rates = {}
    for valve, flow_rate, valves in parse(file):
        connections[valve] = {dst: 1 for dst in valves}
        flow_rates[valve] = flow_rate
    return {valve: {k: (v, flow_rates[k]) for k, v in dijkstra(connections, valve, None)[1].items() if flow_rates[k] > 0 and k != valve} for valve in connections.keys() if flow_rates[valve] > 0 or valve == start_valve}

def restrict_connections(connection_costs, start_valve, allowed_connections):
    return {k: {kk: vv for kk, vv in v.items() if kk in allowed_connections and kk != start_valve} for k, v in connection_costs.items() if k in allowed_connections or k == start_valve}

def create_key(current_valve: str, visited_valves: set[str], time_remaining: int):
    return "".join(sorted([_ for _ in visited_valves])) + current_valve + "-" +  str(time_remaining)

def build_connections(current_valve: str, visited_valves: set[str], time_remaining: int, connection_costs: dict[str, dict[str, tuple[int, int]]], graph: dict[(str, int), dict[(str, int), int]]):
    next_valves = {valve: (time_remaining - travel_cost - 1, flow_rate) for valve, (travel_cost, flow_rate) in connection_costs[current_valve].items()}
    next_valves = {valve: (next_time_remaining, next_time_remaining * flow_rate) for valve, (next_time_remaining, flow_rate) in next_valves.items() if next_time_remaining > 0}
    src = create_key(current_valve, visited_valves, time_remaining)
    if len(next_valves) == 0:
        graph[src] = {}
        return
    else:
        adj = {}
        next = []
        for next_valve, (next_time_remaining, next_pressure) in next_valves.items():
            next_visited_valves = visited_valves.union({current_valve})
            dst = create_key(next_valve, next_visited_valves, next_time_remaining)
            if not dst in graph:
                next.append((next_valve, next_visited_valves, next_time_remaining))
            adj[dst] = -next_pressure
        graph[src] = adj
        for next_valve, next_visited_valves, next_time_remaining in next:
            build_connections(next_valve, next_visited_valves, next_time_remaining, restrict_connections(connection_costs, next_valve, next_valves.keys()), graph)

def calculate_part1(file: str):
    start_valve = "AA"
    connection_costs = get_connection_costs(file, start_valve)
    graph = {}
    build_connections(start_valve, set(), 30, connection_costs, graph)
    _, pressures = dijkstra(graph, create_key(start_valve, set(), 30), None)
    maximal = -min(pressures.values())
    return maximal

def calculate_part2(file: str):
    start_valve = "AA"
    connection_costs = get_connection_costs(file, start_valve)
    graph = {}
    build_connections(start_valve, set(), 26, connection_costs, graph)
    _, pressures = dijkstra(graph, create_key(start_valve, set(), 26), None)
    maximals = {}
    for k, v in pressures.items():
        valves = k.split("-")[0]
        valves_key = "".join(sorted([valves[i:i+2] for i in range(0, len(valves), 2) if valves[i:i+2] != start_valve]))
        if valves_key in maximals:
            maximals[valves_key] = max(maximals[valves_key], -v)
        else:
            maximals[valves_key] = -v
    maximal = 0
    for left, v1 in maximals.items():
        left_len = len(left)
        left_valves = set(left[i:i+2] for i in range(0, len(left), 2) if left[i:i+2])
        for right, v2 in maximals.items():
            right_len = len(right)
            if right_len > left_len: # To skip some checks
                continue
            right_valves = set(right[i:i+2] for i in range(0, len(right), 2) if right[i:i+2])
            if len(left_valves.intersection(right_valves)) == 0:
                maximal = max(maximal, v1 + v2)
    return maximal

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 16, part 1: {}".format(calculate_part1(file)))
    print("Dec 16, part 2: {}".format(calculate_part2(file)))
