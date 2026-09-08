# use Array to solve performance problem if you're dealing the large sequence of numbers
# every object in the array should have the same type
# google python 3 typecode

from array import array

numbers = array("i", [1, 2, 3])
numbers.append(4)  # 4 is object
numbers.remove(1)  # 1 is object
numbers.insert(3, 1)  # 3 is index ; 1 is object
numbers.pop(1)  # 1 is index
print(numbers)
