import sys

try:
    file = sys.argv[1]
except:
    file = "input.txt"

class InfiniteImage:
    def __init__(self, data: list[list[int]], lit_background: bool = False):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
        self.lit_background = lit_background

    def __str__(self) -> str:
        return "\n".join("".join(map(lambda x: "#" if x == 1 else ".", row)) for row in self.data)
    
    def get_index(self, i, j):
        pixels = []
        for k in range(i - 1, i + 2):
            for l in range(j - 1, j + 2):
                if k < 0 or k >= self.rows or l < 0 or l >= self.cols:
                    pixels.append(int(self.lit_background))
                else:
                    pixels.append(self.data[k][l])
        return sum(n * 2**m for m, n in enumerate(reversed(pixels)))
    
    def enhance(self, alg: list[int]):
        data = []
        for i in range(-2, self.rows + 2):
            row = []
            for j in range(-2, self.cols + 2):
                I = self.get_index(i, j)
                row.append(alg[I])
            data.append(row)
        return InfiniteImage(data, bool(alg[0]) if not self.lit_background else bool(alg[len(alg) - 1]))

    def count_lit(self):
        if self.lit_background:
            return None # Infinitely many
        else:
            return sum(sum(row) for row in self.data)

def read(file: str) -> tuple:
    f = open(file, "r")
    img = []
    for i, line in enumerate(map(lambda x: x.strip(), f.readlines())):
        if i == 0:
            iea = [1 if char == "#" else 0 for char in line]
        if i > 1:
            img.append([1 if char == "#" else 0 for char in line])
    return iea, InfiniteImage(img, False)

def enhance(iea: list[int], img: InfiniteImage, n: int):
    if n == 0:
        return img
    else:
        return enhance(iea, img.enhance(iea), n - 1)

iea, data = read(file)

print("Dec 20, part 1: {}".format(enhance(iea, data, 2).count_lit()))
print("Dec 20, part 2: {}".format(enhance(iea, data, 50).count_lit()))
