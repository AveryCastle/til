print("You enter a dark room with two doors. Do you go through door #1 or door #2?")

door = input("> ")


if door == '1':

    print("There's a giant bear here eating a cheese cake. What do you do?")
    print("1. Take the cake.")
    print("2. Scream at the bear.")
    bear = input("> ")
    if bear == "1":
        print("The bear eats your face off. Good job!")
    elif bear == "2":
        print("The bear eats your legs off. Good job!")
    else:
        print("Well, doing %s is probably better. Bear runs away." % bear)
elif door == '2':
    print("2222")
else:
    print("else....")


number = int(input("> "))
if number < 0:
    print("under zero")
elif number > 10:
    print("over 10")
else:
    print("0 < %d < 10 " % number)