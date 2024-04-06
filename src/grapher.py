from src.parser import Entity

class GraphNode :
    
    def __init__(self, entity : Entity):
        self.entity = entity
        self.neighbors = []
        self.score = 0