from sys import argv

script, file_name = argv

txt = open(file_name)

print("Here is %s"%file_name)
print(txt.read())
txt.close()

print("file name again > ")
file_name = input("> ")
txt = open(file_name)

print(txt.read())
txt.close()