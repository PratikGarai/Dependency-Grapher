# main.py

import math
from collections import defaultdict
from src.animals.elephant import Elephant
from ignore.animals.dog import Dog
from src.animals.animals import Animal

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, 0)

    def meow(self):
        print(f"{self.name} says meow!")

def add(a, b):
    return a + b

if __name__ == "__main__":
    e = Elephant("Jumbo", 50)
    e.display()

    c = Cat("Whiskers")
    c.meow()

    d = Dog("Buddy", 50)
    d.bark()