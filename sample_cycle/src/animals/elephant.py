from uuid import uuid4
from src.animals.animals import Animal

N_ELEMENTS = 10

class Elephant(Animal) : 
    def __init__(self, name, age) :
        super().__init__(name, age) 
        self.id = uuid4()

    def display(self) : 
        print("Name: ", self.name)
        print("Age: ", self.age)
        print("ID: ", self.id)