from sys import getsizeof

values = (x * 2 for x in range(100000))
print("gen:", getsizeof(values))

list = [x * 2 for x in range(100000)]
print("list:", getsizeof(list))
