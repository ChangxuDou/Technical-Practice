class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        print(f"{self.x},{self.y}")

point = Point(1,2)

point.draw()