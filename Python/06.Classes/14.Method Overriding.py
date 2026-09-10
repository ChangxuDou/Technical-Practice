class Animal:
    def __init__(self):
        self.age = 1
        print("Animal Constructor")

    def eat(self):
        print("eat")


class Mammal(Animal):
    def __init__(self):
        self.weight = 2
# the constructor defined in Mammal replace the constructor in the base class
        print("Mammal Constructor")
        super().__init__()  # use bilt_in Function super() to  access the base class (animal)

    def walk(self):
        print("walk")


class Fish(Animal):
    def swim(self):
        print("swim")


m = Mammal()
print(m.weight)
