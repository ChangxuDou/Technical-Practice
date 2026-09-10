# if you want to use inheritance ,limit it to one or two level

class Animal:
    def eat(self):
        print("eat")


class Bird(Animal):
    def fly(self):
        print("fly")
