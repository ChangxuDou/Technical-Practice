# google python 3 magic method
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def draw(self):
        print(f"{self.x},{self.y}")


point = Point(10, 20)
other = Point(1, 2)
print(str(point))
print(point)
point.draw()

print(point == other)
print(point > other)
print(point < other)
