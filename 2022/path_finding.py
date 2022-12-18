from typing import TypeVar

T = TypeVar("T")

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

def dijkstra(g: dict[T, dict[T, int]], s: T, t: T) -> tuple[int, dict[T, int]]:
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
