items = [
    ("Product 1", 19),
    ("Product 2", 10),
    ("Product 3", 23)
]

# items.sort(key = lambda parameters: expression)
items.sort(key=lambda item: item[1])
print(items)
