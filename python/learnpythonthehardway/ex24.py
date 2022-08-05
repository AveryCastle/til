print("Let's practice everything.")
print('You\'d need to know \'bout escapes with \\ that do \n newlines and \t tabs.')

poem = """
\tThe lovely world
6 with logic so firmly planted
7 cannot discern \n the needs of love
8 nor comprehend passion from intuition
9 and requires an explanation
10 \n\t\twhere there is none.
"""

print(poem)

five = 10 - 2 + 3 - 6

def secret_formula(started):
    jelly_beans = started * 500
    jars = jelly_beans / 1000
    crates = jars / 100
    return jelly_beans, jars, crates


a, b, c = secret_formula(1000)
print(" %d %d %d" % (a, b, c))