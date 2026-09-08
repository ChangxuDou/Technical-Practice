# set：a collection with no duplicate
# can't access them with index

numbers = [1, 1, 2, 3, 4,]
first = set(numbers)
second = {1, 5, 6}
second.add(7)
second.remove(6)
print(len(second))
print(second)

print(first)
print(first | second)  # union of two sets 全集
print(first & second)  # intersection of two sets 交集
print(first - second)  # item in first ,but not in second
print(first ^ second)  # either in first or second set
