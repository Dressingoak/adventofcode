# import numpy as np
# import matplotlib.pyplot as plt

Point = tuple[int, int]
Line = tuple[Point, Point]

def det(a: int, b: int, c: int, d:int):
    return a * d - b * c

def dist(p1: Point, p2: Point):
    match (p1, p2):
        case ((x1, y1), (x2, y2)):
            return abs(x2 - x1) + abs(y2 - y1)

def intersection(l1: Line, l2: Line, l1_inf: bool = False, l2_inf: bool = False) -> Point | None:
    match (l1, l2):
        case (((x1, y1), (x2, y2)), ((x3, y3), (x4, y4))):
            t_num = det(x1 - x3, x3 - x4, y1 - y3, y3 - y4)
            t_den = det(x1 - x2, x3 - x4, y1 - y2, y3 - y4)
            u_num = det(x1 - x3, x1 - x2, y1 - y3, y1 - y2)
            u_den = det(x1 - x2, x3 - x4, y1 - y2, y3 - y4)
            if t_den == 0 or u_den == 0:
                return None
            t, u = t_num / t_den, u_num / u_den
            if (l1_inf or (t >= 0 and t <= 1)) and (l2_inf or (u >= 0 and u <= 1)):
                x = x1 + t_num * (x2 - x1) // t_den
                y = y1 + t_num * (y2 - y1) // t_den
                return (x, y), t_num, t_den, u_num, u_den
            else:
                return None

class Polygon:
    def __init__(self, points: list[Point]):
        self.points = points

    def vertex_order(self):
        return sum((x2 - x1) * (y2 + y1) for ((x1, y1), (x2, y2)) in self.edges())

    def __eq__(self, other):
        return set(self.verticies()) == set(other.verticies()) and self.vertex_order() == other.vertex_order()

    def verticies(self, start: int = 0):
        n = len(self.points)
        for i in range(start, start + n):
            yield self.points[i%n]

    def edges(self, start: int = 0):
        n = len(self.points)
        for i in range(start, start + n):
            yield (self.points[i%n], self.points[(i+1)%n])

    def on_border(self, p: Point) -> bool:
        for (p3, p4) in self.edges():
            if dist(p3, p4) == dist(p3, p) + dist(p, p4):
                return True
        return False

    def contains(self, p: Point) -> bool:
        l1 = ((p[0] + 100, p[1]), p)
        wn = 0
        intersections = set()
        for (p3, p4) in self.edges():
            if dist(p3, p4) == dist(p3, p) + dist(p, p4):
                return True
            if p3 in intersections or p4 in intersections:
                continue
            c = intersection(l1, (p3, p4))
            match c:
                case None: pass
                case (x, y), _, _, _, _:
                    intersections.add((x, y))
                    wn += 1
        return wn % 2 != 0

    def insert_intersections(self, other):
        vertices = []
        all_intersections = set()
        for vs in self.edges():
            # print(f"vs: {vs}")
            if len(vertices) == 0 or vertices[-1] != vs[0]:
                vertices.append(vs[0])
            intersections = []
            for vo in other.edges():
                # print(f"- vo: {vo}")
                match intersection(vs, vo):
                    case None: pass
                    case (x, y), t_num, t_den, _, _:
                        intersections.append((t_num / t_den, (x, y)))
            intersections.sort()
            all_intersections.update([c for _, c in intersections])
            for _, c in intersections:
                if vertices[-1] != c:
                    vertices.append(c)
        return all_intersections, Polygon(vertices)

    def union(self, other):
        intersections, polyA = self.insert_intersections(other)
        _, polyB = other.insert_intersections(self)
        # print(intersections)
        outside = set(vs for vs in polyA.verticies() if not polyB.contains(vs))
        if len(outside) == len(set(polyA.points)):
            yield Polygon([vs for vs in polyA.verticies()])
            yield Polygon([vo for vo in polyB.verticies()])
        elif len(outside) == 0:
            yield Polygon([vo for vo in polyB.verticies()])
        else:
            # print(outside)
            while len(outside) > 0:
                verts = []
                start = outside.pop()
                # print(f"Start: {start}")
                polygons = [polyA, polyB]
                v, p = start, 0
                returned = False
                while not returned:
                    i = polygons[p].points.index(v)
                    for vertex in polygons[p].verticies(i + 1):
                        # print(f"""At vertex {vertex} in polygon {"A" if p == 0 else "B"}""")
                        verts.append(vertex)
                        if vertex in outside:
                            outside.remove(vertex)
                        if vertex in intersections:
                            # print("At intersection, shift...")
                            v = vertex
                            p += 1
                            p %= 2
                            break
                        elif vertex == start:
                            returned = True
                            break
                yield Polygon(verts)
                # print(f"Broke out, have verticies: {verts}, still outside: {outside}")

    def union_all(self, *other):
        pass
            

    
    def from_sensor_and_beacon(sensor: Point, beacon: Point):
        match (sensor, beacon):
            case ((sx, sy), (bx, by)):
                dist = abs(bx - sx) + abs(by - sy)
                return Polygon([
                    (sx, sy + dist),
                    (sx + dist, sy),
                    (sx, sy - dist),
                    (sx - dist, sy)
                ])

    # def to_numpy(self):
    #     return np.array([x for x, _ in self.points]), np.array([y for _, y in self.points])

poly1 = Polygon([
    (1, 1),
    (1, 13),
    (5, 9),
    (3, 7),
    (5, 5)
])

poly2 = Polygon([
    (5, 3),
    (5, 11),
    (11,11),
    (11, 3)
])

poly3 = Polygon([
    (4,  2),
    (4, 12),
    (12,12),
    (12, 2)
])

poly4 = Polygon([
    (-4,  -2),
    (-4, -12),
    (-12,-12),
    (-12, -2)
])

for poly in poly3.union(poly4):
    print(f"Polygon: {poly.points}, order: {poly.vertex_order()}")

# poly = Polygon.from_sensor_and_beacon((8, 7), (2, 10))
# print(poly.contains((3, -2)))

# plt.figure(figsize=(4, 4))
# plt.axis('equal')

# poly = Polygon.from_sensor_and_beacon((8, 7), (2, 10))
# x, y = poly.to_numpy()
# plt.fill(x, y, "b", alpha=0.5)

# poly = Polygon.from_sensor_and_beacon((10, 10), (3, 10))
# x, y = poly.to_numpy()
# plt.fill(x, y, "b", alpha=0.5)

# plt.grid(True)
# plt.show()
