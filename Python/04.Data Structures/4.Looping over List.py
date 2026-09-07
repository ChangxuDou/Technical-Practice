letters = ['a', 'b', 'c', 'd']
for letter in letters:
    print(letter)

# what if we want the index of each items
letters = ['a', 'b', 'c', 'd']
for letter in enumerate(letters):
    print(letter)

# use enumerate : for each iteration,this enumerate will give us a tuple (read only).


# what if we only want the index or the item:
letters = ['a', 'b', 'c', 'd']
for letter in enumerate(letters):
    print(letter[0], letter[1])

# want syntax more beautiful:
letters = ['a', 'b', 'c', 'd']
for index, letter in enumerate(letters):
    print(index, letter)
