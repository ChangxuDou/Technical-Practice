numbers = [3, 51, 2, 8, 6]
# numbers.sort(reverse = True)
print(sorted(numbers))  # sorted will return a new list
print(numbers)


# sort a list of tuple
items = [
    ("Product 1", 19),
    ("Product 2", 10),
    ("Product 3", 23)
]


def sort_item(item):
    return item[1]


items.sort(key=sort_item)
print(items)
