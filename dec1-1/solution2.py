data = list(map(lambda x: int(x), open("data.txt").readlines()))

for (i, left) in enumerate(data):
    for right in data[(i+1):]:
        if (left + right == 2020):
            print(left * right)
