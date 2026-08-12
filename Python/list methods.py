numbers = [2,34,56,34,2,34,3,45,3,4,56,367]
numbers1= []
for number in numbers:
    if numbers.count(number) > 1:
        numbers1.append(number)
print(numbers1)
print(numbers)




