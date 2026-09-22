import numpy as np

# array = np.array([[1,2,3],[4,5,6]])
# print(array)
# print(type(array))
# print(array.shape)

# initialization with zero or one.
array = np.zeros((3, 4), dtype=int)  # parameter"dtype" is optional
array = np.ones((3, 4))
array = np.full((3, 4), 5, dtype=int)
array = np.random.random((3, 4))
print(array)
print(array[1, 1])  # array[1][1] the code in python looks like this
print(array > 0.5)
print(array[array > 0.5])
print(np.sum(array))
print(np.floor(array))  # 向下取整
print(np.ceil(array))  # 向上取整
print(np.round(array))

# arthmetic operation between array and numbers
first = np.array([1, 2, 3])
second = np.array([1, 2, 3])
print(first+second)
print(first+2)

dimensions_inch = np.array([1, 2, 3])
dimensions_cm = dimensions_inch * 2.54
print(dimensions_cm)

# pure python code without NumPy
dimensions_inch = [1, 2, 3]
dimensions_cm = [x * 2.54 for x in dimensions_inch]
print(dimensions_cm)
