def det(a, b, c, d):
    return a * d - b * c


def part1(file: str, least=200000000000000, most=400000000000000):
    hailstorms = []
    with open(file) as f:
        for line in f:
            p, v = line.strip().split("@")
            hailstorms.append(
                ([int(_) for _ in p.split(", ")], [int(_) for _ in v.split(", ")])
            )
    count = 0
    for i, hs1 in enumerate(hailstorms):
        x1, y1 = hs1[0][:2]
        x2, y2 = x1 + hs1[1][0], y1 + hs1[1][1]
        for hs2 in hailstorms[i + 1 :]:
            x3, y3 = hs2[0][:2]
            x4, y4 = x3 + hs2[1][0], y3 + hs2[1][1]

            t = det(x1 - x3, x3 - x4, y1 - y3, y3 - y4)
            u = det(x1 - x3, x1 - x2, y1 - y3, y1 - y2)
            d = det(x1 - x2, x3 - x4, y1 - y2, y3 - y4)
            match d:
                case 0:
                    continue
                case _ if d > 0:
                    if t < 0 or u < 0:
                        continue
                    if least * d > x1 * d + t * (x2 - x1):
                        continue
                    if most * d < x1 * d + t * (x2 - x1):
                        continue
                    if least * d > y1 * d + t * (y2 - y1):
                        continue
                    if most * d < y1 * d + t * (y2 - y1):
                        continue
                case _:
                    if t > 0 or u > 0:
                        continue
                    if least * d < x1 * d + t * (x2 - x1):
                        continue
                    if most * d > x1 * d + t * (x2 - x1):
                        continue
                    if least * d < y1 * d + t * (y2 - y1):
                        continue
                    if most * d > y1 * d + t * (y2 - y1):
                        continue
            count += 1

    return count


def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


class Fraction:
    def __init__(self, a, b=1):
        if b < 0:
            div = gcd(-a, -b)
            self.a, self.b = -a // div, -b // div
        else:
            div = gcd(a, b)
            self.a, self.b = a // div, b // div

    def __neg__(self):
        return Fraction(-self.a, self.b)

    def __int__(self):
        return self.a // self.b

    def __add__(self, other):
        if isinstance(other, int):
            c, d = other, 1
        else:
            c, d = other.a, other.b
        return Fraction(self.a * d + c * self.b, self.b * d)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, int):
            c, d = other, 1
        else:
            c, d = other.a, other.b
        return Fraction(self.a * c, self.b * d)

    def __truediv__(self, other):
        if isinstance(other, int):
            c, d = other, 1
        else:
            c, d = other.a, other.b
        return Fraction(self.a * d, self.b * c)

    def __rtruediv__(self, other):
        return self / other

    def __abs__(self):
        return Fraction(-self.a if self.a < 0 else self.a, self.b)

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            c, d = other, 1
        else:
            c, d = other.a, other.b
        return self.a == c and self.b == d

    def __lt__(self, other):
        if isinstance(other, int):
            c, d = other, 1
        else:
            c, d = other.a, other.b
        return self.a * d < c * self.b

    def __repr__(self):
        if self.b == 1:
            return f"{self.a}"
        else:
            return f"{self.a}/{self.b}"


def gauss_jordan_elimination(A):
    n, m = len(A), len(A[0])
    h, k = 0, 0
    while h < n and k < m:
        i_max = max((i for i in range(h, n)), key=lambda i: abs(A[i][k]))  # argmax
        if A[i_max][k] == 0:
            k += 1
        else:
            A[i_max], A[h] = A[h], A[i_max]  # swap rows
            for i in range(h + 1, n):
                f = A[i][k] / A[h][k]
                A[i][k] = Fraction(0)
                for j in range(k + 1, m):
                    A[i][j] -= A[h][j] * f
            h += 1
            k += 1
    if any(A[h][h] == 0 for h in range(n)):
        raise ValueError("Non-invertible matrix")
    for h in reversed(range(0, n)):
        for j in reversed(range(h, m)):
            A[h][j] /= A[h][h]
        for i in reversed(range(0, h)):
            f = A[i][h]
            A[i][h] = Fraction(0)
            for j in range(n, m):
                A[i][j] -= A[h][j] * f
    return A


def solve_linear_system(A, c):
    argmented = []
    for i in range(len(A)):
        argmented.append([Fraction(_) for _ in A[i]] + [Fraction(_) for _ in c[i]])
    gauss_jordan_elimination(argmented)
    return [argmented[i][len(A) :] for i in range(len(A))]


def part2(file: str):
    hailstorms = []
    with open(file) as f:
        for line in f:
            p, v = line.strip().split("@")
            hailstorms.append(
                ([int(_) for _ in p.split(", ")], [int(_) for _ in v.split(", ")])
            )

    A, c = [], []  # A * x = c
    for i, j in [(0, 1), (0, 2)]:
        for d1, d2 in [[0, 1], [0, 2], [1, 2]]:  # (x,y), (x,z), (y,z)
            c.append(
                [
                    hailstorms[j][0][d1] * hailstorms[j][1][d2]
                    - hailstorms[j][0][d2] * hailstorms[j][1][d1]
                    - (
                        hailstorms[i][0][d1] * hailstorms[i][1][d2]
                        - hailstorms[i][0][d2] * hailstorms[i][1][d1]
                    )
                ]
            )
            row = [0] * 6
            row[d1] = -(hailstorms[i][1][d2] - hailstorms[j][1][d2])  # p_d1
            row[d2] = hailstorms[i][1][d1] - hailstorms[j][1][d1]  # p_d2
            row[d1 + 3] = hailstorms[i][0][d2] - hailstorms[j][0][d2]  # v_d1
            row[d2 + 3] = -(hailstorms[i][0][d1] - hailstorms[j][0][d1])  # v_d2
            A.append(row)

    x = solve_linear_system(A, c)

    p1, p2, p3 = x[0][0], x[1][0], x[2][0]
    return int(p1 + p2 + p3)


if __name__ == "__main__":
    print(f"{part1('input.txt')=}")
    print(f"{part2('input.txt')=}")
