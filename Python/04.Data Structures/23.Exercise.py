# find the most repeatable character in this text
sentence = "This is a commen interview question"


# list, tuple, array, set, dict
letters = [*sentence]
times = 0
for letter in sentence:
    time = sentence.count(letter)
    print(time, letter)
    if time > times:
        times = time
    print(times, letter)
