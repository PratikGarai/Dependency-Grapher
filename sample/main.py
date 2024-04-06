# main.py

import math
from collections import defaultdict
from src.elephant import Elephant
from ignore.dog import Dog

class Cat:
    def __init__(self, name):
        self.name = name

    def meow(self):
        print(f"{self.name} says meow!")

def add(a, b):
    return a + b

if __name__ == "__main__":
    e = Elephant("Jumbo", 50)
    e.display()

    c = Cat("Whiskers")
    c.meow()

    d = Dog("Buddy")
    d.bark()