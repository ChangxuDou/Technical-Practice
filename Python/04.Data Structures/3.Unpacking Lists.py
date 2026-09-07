numbers = [1, 2, 3, 4, 5]
first = numbers[0]
second = numbers[1]
third = numbers[2]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# in this example,we have both unpacking and packing
first, second, third, *other, last = numbers
print(other)
print(second)
print(last)

# packing -- just like use function to pack a list, but the result is tuple


def multiply(*numbers):
    return numbers


result = multiply(1, 2, 3, 4, 5, 6)
print(result)
