from functools import reduce

input_data = list(map(lambda x: x.split(), "".join(open("input.txt").readlines()).split('\n\n')))

class Answer:

    def __init__(self, answer: str):
        self.answer = set(char for char in answer)

    def __str__(self):
        return "".join(sorted(self.answer))
    
    def __repr__(self):
        return "Answer<{}>".format(self.__str__())

    def count(self):
        return len(self.answer)

class Group:

    def __init__(self, answers: list[Answer]):
        self.answers = answers

    def __repr__(self):
        return "Group<{}>".format(", ".join([_.__str__() for _ in self.answers]))

    def union_answers(self):
        return Answer("".join(reduce(lambda x, y: x.union(y), [_.answer for _ in self.answers])))

    def intersect_answers(self):
        return Answer("".join(reduce(lambda x, y: x.intersection(y), [_.answer for _ in self.answers])))

groups = [Group(list(Answer(_) for _ in answers)) for answers in input_data]

print("Part 1: {}".format(sum(_.union_answers().count() for _ in groups)))
print("Part 2: {}".format(sum(_.intersect_answers().count() for _ in groups)))
