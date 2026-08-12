state = ""
while True:
    command = input('>').upper()
    if command == "HELP":
        print("""
            start -to start the car
            stop  - to stop the car"
            quit  - to exit
            """)
    elif command == "START":
        if state != 1:
            state = 1
            print("Car started .... Ready to go")
        else :
            print("Car is already running")
    elif command == "STOP":
        if state != 0:
            state = 0
            print("The car stopped")
        else:
            print("The car is already stopped")
    elif command == "QUIT":
        break
    else:
        print('I don not understand')