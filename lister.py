from src.explorer import Explorer
from src.parser import Entity
from src.grapher import Grapher

if __name__ == "__main__":
    root = "sample"
    ignore_list = ["ignore"]
    
    grapher = Grapher(root_folder=root, ignore_list=ignore_list)

    # for entity in grapher.entities:
    #     entity.display()

    grapher.get_graph()
