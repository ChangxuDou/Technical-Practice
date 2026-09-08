letters = ['a', 'b', 'c', 'd']
# add
letters.append("e")  # add items in the end
letters.insert(0, "-")  # add item at a specific positon

# remove
# pop M remove the item at the end. With index can remove item at specific position
letters.pop(0)
letters.remove("b")  # remove the object and don't konw the index

del letters[0:3]  # delete one or a range of items
letters.clear()  # delete all items
print(letters)
