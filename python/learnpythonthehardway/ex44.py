class Parent(object):
    def implicit(self):
        print("Parent aaaaa")


class Child(Parent):
    def implicit(self):
        super().implicit()
        print("child aaaa")

# dad = Parent()
child = Child()

# dad.implicit()
child.implicit()