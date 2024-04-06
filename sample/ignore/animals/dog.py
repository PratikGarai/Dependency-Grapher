from uuid import uuid4

class Dog:
    def __init__(self, name):
        self.name = name
        self.id = uuid4()

    def bark(self):
        print(f"{self.name} with id {str(self.id)} says woof!")