input_data = list(map(lambda x: x.replace('\n', ""), open("input.txt").readlines()))

class toboggan:

    data = input_data
    width = len(data[0])

    def __init__(self, right, down):
        self.right = right
        self.down = down
    
    def traverse(self):
        trees = 0
        col = 0



        for row in range(0, len(self.data), self.down)[1:]:
            col += self.right 
            col %= self.width

            trees += int(self.data[row][col] == "#")
        
        return trees

res = toboggan(1, 1).traverse() * toboggan(3, 1).traverse() * toboggan(5, 1).traverse() * toboggan(7, 1).traverse() * toboggan(1, 2).traverse()
print(res)
