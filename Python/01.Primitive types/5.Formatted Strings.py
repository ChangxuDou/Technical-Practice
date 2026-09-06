course = "  Python Programming "
print(course.upper())
print(course.lower())

print(course.title()) 
# title is a method that capitalizes the first letter of each word in a string.

print(course.strip())
# strip is a method that removes any whitespace from the beginning and end of a string.

print(course.lstrip())
# lstrip is a method that removes any whitespace from the beginning of a string.
print(course.rstrip())
# rstrip is a method that removes any whitespace from the end of a string.

print(course.find("Pro"))
# find is a method that returns the index of the first occurrence of a substring in a string. If the substring is not found, it returns -1.

print(course.replace("Python", "Java"))
# replace is a method that replaces all occurrences of a substring with another substring in a string.

print("pro" in course)
# The 'in' operator checks if a substring exists within a string and returns True or False.

print("Python" not in course)
# The 'not in' operator checks if a substring does not exist within a string and returns