def print_two(*args):
    arg1, arg2 = args
    print("%r %r " % (arg1, arg2))

def print_one(arg1):
    print("arg1 = %r" % arg1)

print_two("V", "jimin")

print_one("v")