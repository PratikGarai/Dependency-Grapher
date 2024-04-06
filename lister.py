from src.explorer import Explorer
from src.parser import Entity

if __name__ == "__main__":
    explorer = Explorer("sample", ["ignore"])
    py_files = explorer.explore()
    print(py_files)

    entities: list[Entity] = []
    for file in py_files:
        entity = Entity(file)
        entity.parse()
        entities.append(entity)

    for entity in entities:
        entity.display()
