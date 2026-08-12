secret_number = 9
guess_count = 0
guess_limit = 3
while guess_count < guess_limit :
    number = int(input("number:"))
    guess_count += 1
    if number == secret_number:
        print("you win!")
        break
else:
    print("you lost your 3 chances")


