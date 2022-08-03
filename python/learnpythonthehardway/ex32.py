the_count = [1, 2, 3, 4, 5]

fruits = ['apples', 'oranges', 'pears', 'apricots']

change = [1, 'pennies', 2, 'dimes', 3, 'quarters']

for count in the_count:
    print("%d " %  count)

for value in change:
    print("%r" % value)

element = []

for number in range(1, 10):
    element.append(number)

for value in element:
    print(value)

array = []
element = []
for value in range(1, 7):
    element.append(value)
    if value == 3:
        array.append(element)
        element = []
    if value == 6:
        array.append(element)



