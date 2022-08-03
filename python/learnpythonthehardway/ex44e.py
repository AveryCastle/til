class Other(object):
    def __init__(self):
        pass

    def override(self):
        print("Other override")

    def implicit(self):
        print("Other implicit")

    def alter(self):
        print("Other alter")


class Child(object):
    def __init__(self):
        self.other = Other()

    def override(self):
        print("Child override")

    def implicit(self):
        self.other.implicit()

    def alter(self):
        print("CHILD, BEFORE OTHER altered()")
        self.other.alter()
        print("CHILD, AFTER OTHER altered()")


other = Other()
other.override()
other.implicit()
other.alter()
print("-======")
child = Child()
child.override()
child.implicit()
child.alter()
