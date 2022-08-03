people = 20

dog = 30
cats = 10

if people < 20:
    print(f"people is under {people}.")
elif people == 20:
    print("people is %d" % people)
elif people >= 20:
    print("people is %d" % people)
else:
    print("people is over %d" % people)


dog += 5
if dog >= 35:
    print(dog)