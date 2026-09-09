try:
    with open("app.py") as file:
        # the object File support context management protocol (enter,exit)
        print("File opened")
    age = int(input("Age: "))
    xfactor = 10/age
except (ValueError, ZeroDivisionError):
    print("You didn't enter a valid age.")
else:
    print("No exception were thrown")
