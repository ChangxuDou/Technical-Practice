count = 0
for number in range(1,10):
    if number % 2 == 0:
        print(number)
        count += 1
print(f"there are {count} even_number")

even_num= []
for number in range(1,10):
    if number % 2 == 0:
        print(number)
        even_num.append(number)
print(f"there are {len(even_num)} even numbers")
