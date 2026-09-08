# list
values = []
for x in range(5):
    values.append(x * 2)

values = [x * 2 for x in range(5)]
print(values)

# set
values = set()
for x in range(5):
    values.add(x * 2)
values = {x * 2 for x in range(5)}  # simpler
print(values)

# dict
values = {}
for x in range(5):
    values[x] = x * 2

values = {x: x * 2 for x in range(5)}  # simpler
print(values)
