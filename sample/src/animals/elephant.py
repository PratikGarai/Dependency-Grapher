from uuid import uuid4

N_ELEMENTS = 10

class Elephant : 
    def __init__(self, name, age) : 
        self.name = name
        self.age = age
        self.id = uuid4()

    def display(self) : 
        print("Name: ", self.name)
        print("Age: ", self.age)
        print("ID: ", self.id)