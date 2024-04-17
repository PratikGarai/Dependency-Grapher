from src.animals.elephant import Elephant

class AfricanElephant(Elephant):
    def __init__(self, name):
        super().__init__(name)
        self.species = "Loxodonta africana"

    def get_species(self):
        return self.species