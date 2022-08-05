# users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}
#
# for user, status in users.copy().items():
#     if status == 'inactive':
#         del users[user]
#
# print(users)
#
# list = list(range(1, 5))
# print(list)

def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)


class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self,iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update


class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)

mappingClass = MappingSubclass([1,2,3, 4,5,6])
mappingClass.update([10, 20], [100, 200])
print(mappingClass.items_list)


xvec = [10, 20, 30]
yvec = [7, 5, 3]
sum = sum(x + y for x, y in zip(xvec, yvec))
print(sum)