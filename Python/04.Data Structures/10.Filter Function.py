items = [
    ("Product 1", 19),
    ("Product 2", 10),
    ("Product 3", 23)
]

filtered = list(filter(lambda item: item[1] > 10, items))
print(filtered)
