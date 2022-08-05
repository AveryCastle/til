def test_generator():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5

gen = test_generator()

print(type(gen))

# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))

for value in test_generator():
    print(value)

def infinit_generator():
    count = 0
    while True:
        count += 1
        yield count

infinit_gen = infinit_generator()
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
print(next(infinit_gen))
