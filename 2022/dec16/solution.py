import sys
import re

class MinPriorityQueue:
    def __init__(self) -> None:
        self.keys = dict()
        self.data = []

    def __len__(self):
        return len(self.data)

    def swap(self, i, j):
        self.keys[self.data[i][0]], self.keys[self.data[j][0]] = j, i
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def sift_up(self, i):
        if i == 0:
            return
        j = (i - 1) // 2
        match [self.data[i][1], self.data[j][1]]:
            case [None, x]: return
            case [x, y] if y is None or x < y:
                self.swap(i, j)
                self.sift_up(j)

    def sift_down(self, i):
        children = [j for j in [2 * i + 1, 2 * i + 2] if j < len(self.data) and self.data[j][1] is not None]
        if len(children) > 0:
            j = min(children, key = lambda k: self.data[k][1])
            if self.data[i][1] is None or self.data[j][1] < self.data[i][1]:
                self.swap(i, j)
                self.sift_down(j)
    
    def insert(self, key, value):
        if key in self.keys:
            i = self.keys[key]
            self.data[i] = (key, value)
        else:
            i = len(self.data)
            self.data.append((key, value))
            self.keys[key] = i
        self.sift_up(i)

    def pop(self):
        if len(self.data) > 0:
            self.swap(0, len(self.data) - 1)
            key, value = self.data.pop()
            self.sift_down(0)
            del self.keys[key]
            return (key, value)
        else:
            return

def dijkstra(g: dict[int, dict[int, int]], s: int, t: int) -> int:
    Q = MinPriorityQueue()
    dist = dict()
    for v in g.keys():
        Q.insert(v, None)
        dist[v] = None
    dist[s] = 0
    Q.insert(s, 0)
    while len(Q) > 0:
        u, d = Q.pop()
        if u == t:
            return (d, dist)
        for v, x in g[u].items():
            try:
                alt = dist[u] + x
            except:
                return (None, dist)
            if dist[v] is None or alt < dist[v]:
                dist[v] = alt
                Q.insert(v, alt)
    return (None, dist)

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

def move(current_valve, time_remaining, pressure, connection_costs):
    next_valves = {valve: (time_remaining - travel_cost - 1, flow_rate) for valve, (travel_cost, flow_rate) in connection_costs[current_valve].items()}
    next_valves = {valve: (next_time_remaining, pressure + next_time_remaining * flow_rate) for valve, (next_time_remaining, flow_rate) in next_valves.items() if next_time_remaining > 0}
    if len(next_valves) == 0:
        yield pressure
    else:
        for next_valve, (next_time_remaining, next_pressure) in next_valves.items():
            next_connection_costs = restrict_connections(connection_costs, next_valve, next_valves.keys())
            yield from move(next_valve, next_time_remaining, next_pressure, next_connection_costs)

def combination(arr, n, r, index, data, i):
    if(index == r):
        yield data[:r]
    elif(i < n):
        data[index] = arr[i]
        yield from combination(arr, n, r, index + 1, data, i + 1)
        yield from combination(arr, n, r, index, data, i + 1)

def subsets(arr, size):
    n = len(arr)
    data = list(range(size))
    yield from combination(arr, n, size, 0, data, 0)

def unique_splits_half(arr):
    n = len(arr)
    for i in range(n // 2 + 1):
        if i == n // 2 and n % 2 == 0:
            arrs = [subset for subset in subsets(arr, i)]
            m = len(arrs) // 2
            yield from arrs[:m]
        else:
            yield from subsets(arr, i)

def unique_splits(arr):
    arr_set = set(arr)
    for split in unique_splits_half(arr):
        left = set(split)
        right = arr_set.difference(left)
        yield (left, right)

def distribute_connections(connection_costs, start_valve):
    valves = [valve for valve in connection_costs.keys() if valve != start_valve]
    for left, right in unique_splits(valves):
        yield (restrict_connections(connection_costs, start_valve, left), restrict_connections(connection_costs, start_valve, right))

def calculate_part1(file: str):
    start_valve = "AA"
    connection_costs = get_connection_costs(file, start_valve)
    return max(move(start_valve, 30, 0, connection_costs))

def calculate_part2(file: str):
    start_valve = "AA"
    connection_costs = get_connection_costs(file, start_valve)
    m = 0
    # total = sum(1 for _ in unique_splits_half([valve for valve in connection_costs.keys() if valve != start_valve]))
    for i, (left, right) in enumerate(distribute_connections(connection_costs, start_valve)):
        m = max(m, max(move(start_valve, 26, 0, left)) + max(move(start_valve, 26, 0, right)))
        # print(f"progress: {i+1} / {total}")
    return m

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except:
        file = "input.txt"

    print("Dec 16, part 1: {}".format(calculate_part1(file)))
    print("Dec 16, part 2: {}".format(calculate_part2(file)))
