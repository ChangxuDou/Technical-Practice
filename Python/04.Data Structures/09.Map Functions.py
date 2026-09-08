items = [
    ("Product 1", 19),
    ("Product 2", 10),
    ("Product 3", 23)
]

# prices = []
# for item in items:
#     prices.append(item[1])
# print(prices)

price = list(map(lambda item: item[1], items))
print(price)
