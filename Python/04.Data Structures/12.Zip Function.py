list1 = [1, 2, 3]
list2 = [10, 20, 30]

# we want to combine these two lists to a list of tuple like this [(1,10),(2,20),(3,30)]
print(list(zip(list1, list2)))

print(list(zip("abc", list1, list2)))
