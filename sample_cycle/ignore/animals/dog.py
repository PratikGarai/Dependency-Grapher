from uuid import uuid4
from src.animals.animals import Animal

class Dog(Animal):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.id = uuid4()

    def bark(self):
        print(f"{self.name} with id {str(self.id)} says woof!")