def multiply(x, y):
    return x * y


print(multiply(2, 3))

# what if we want to pass more than 2 arguments ?


def multiply(*numbers):
    total = 1
    for number in numbers:
        total *= number
    return total


print(multiply(2, 3, 4, 5))
