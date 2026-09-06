# fizz_buzz
# if the number is divisible by 3, print "Fizz"
# if the number is divisible by 5, print "Buzz"
# if the number is divisible by both 3 and 5, print "FizzBuzz"
# if the number is not divisible by 3 or 5, print the number

def fizz_buzz(number):
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return str(number)


print(fizz_buzz(30))  # 3,5,30,17
