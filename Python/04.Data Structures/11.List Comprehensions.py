items = [
    ("Product 1", 19),
    ("Product 2", 10),
    ("Product 3", 23)
]

# price = list(map(lambda item: item[1], items))
price = [item[1] for item in items]  # only available in python
print(price)

# filtered = list(filter(lambda item: item[1] > 10, items))
filtered = [item for item in items if item[1] > 10]  # only available in python
print(filtered)
