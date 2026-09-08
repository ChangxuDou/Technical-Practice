# find the most repeatable character in this text
sentence = "This is a commen interview question"
sentence = sentence.lower()
sentence = sentence.strip()
sentence = sentence.replace(" ", "")
letters = [*sentence]  # unpack to list
# print(letters)

dic = {}
for letter in letters:
    dic[letter] = dic.get(letter, 0) + 1

# First
sorted = sorted(dic, key=lambda letter: dic[letter], reverse=True)
print(sorted)

# Second
sorted_items = sorted(dic.items(), key=lambda dic: dic[1], reverse=True)
print(sorted_items)

# -------------------------------

sentence = "This is a commen interview question"
sentence = sentence.lower()
sentence = sentence.strip()
sentence = sentence.replace(" ", "")
letters = [*sentence]  # unpack to list

max_time = 0
max_letter = ""

for letter in letters:
    time = letters.count(letter)

    if time > max_time:
        max_time = time
        max_letter = letter
print(max_letter, max_time)
