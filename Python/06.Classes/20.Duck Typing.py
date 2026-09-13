# Python is a dynamically typed language and doesn't check the type of object.

class Textbox:
    def draw(self):
        print("Textbox")


class DropDownList:
    def draw(self):
        print("DropDownList")


def draw(controls):
    for control in controls:
        control.draw()


ddl = DropDownList()
textbox = Textbox()
draw([ddl, textbox])
