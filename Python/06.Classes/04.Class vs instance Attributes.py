class Point:
    default_color = "red"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        print(f"{self.x},{self.y}")


point = Point(1, 2)
print(point.x)
print(point.default_color)
print(Point.default_color)
point.draw()

# class level attributes are shared across all instances of a class
another = Point(3, 4)
print(another.x, another.y)
another.draw()
