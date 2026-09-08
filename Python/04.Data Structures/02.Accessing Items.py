letters = ["a", "b", "c", "d"]
print(letters[0])
print(letters[0:3])
print(letters[-1])
print(letters[::2])

numbers = list(range(20))
# :: means start:stop:step, so 2 means take every second element
print(numbers[::2])
print(numbers[::-1])  # :: means start:stop:step, so -1 means reverse the list
print(numbers[::-2])  # reverse the list and take every second element]
