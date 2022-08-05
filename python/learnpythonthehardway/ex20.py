from sys import argv

script, file_name = argv

def print_all(f):
    print(f.read())

def rewind(f):
    f.seek(0)

def print_a_line(line_count, f):
    print(line_count, f.readline())

file = open(file_name)

print_all(file)

rewind(file)

current_line = 1
print_a_line(current_line, file)

current_line += 1
print_a_line(current_line, file)

current_line += 1
print_a_line(current_line, file)