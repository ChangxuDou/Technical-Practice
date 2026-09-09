# google python 3 magic method
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def draw(self):
        print(f"{self.x},{self.y}")


point = Point(1, 2)
print(str(point))
print(point)
point.draw()
