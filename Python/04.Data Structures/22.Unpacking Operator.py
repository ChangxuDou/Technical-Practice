# unpack any iterables

# list
first = [1, 2]
second = [3]
values = [*range(5), *"hello"]
print(values)

# dict
first = {"x": 1}
second = {"x": 10, "y": 20}
combined = {**first, **second, "z ": 1}
print(combined)
