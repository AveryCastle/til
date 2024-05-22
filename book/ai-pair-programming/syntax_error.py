class MyClass:
  def __init__(self, name, age) -> None:
    self.name = name
    self.age = age
    
  def print_info(self):
    print(f"Name: {self.name}, Age: {self.age}")
  
def main():
  people = [
    MyClass("Alice", 25),
    MyClass("Bob", 30),
    MyClass("Charlie", 35),
  ]

  for person in people:
    person.print_info()
    
  print("Total people:", len(people))
  
  with open("people.txt", "r") as file:
    content = file.read()
    print("File content:", {content})
    
  x = lambda a, b: a + b
  print("Lambda result: ", x(5, 10))
  
if __name__ == "__main__":
  main()