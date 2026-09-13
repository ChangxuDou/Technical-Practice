# if the classes have only data no method no behavior, use nametuple
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)

# ------


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)
