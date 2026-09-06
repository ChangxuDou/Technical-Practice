def greet(name):
    print(f"Hello, {name}!")

# 1-Perform a task ---- like above example
# 2-Return a value ---- round(1.9)


def get_greeting(name):
    return f"Hello, {name}!"


message = get_greeting("Mosh")
file = open("greeting.txt", "w")
file.write(message)
file.close()
