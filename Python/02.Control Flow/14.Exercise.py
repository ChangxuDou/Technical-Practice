# write a program to display the even numbers from 1 to 9
# and return "We have 4 even numbers"

count = 0
for number in range(1, 10):
    if number % 2 == 0:
        print(number)
        count += 1
print(f"We have {count} even numbers")
