import os

import networkx as nx

from src.explorer import Explorer
from src.entity import Entity


class Grapher:
    '''
    Parse the entities that are given and create a graph based on imports.

    Attributes:
    -----------
    root_folder : str
        The root folder to start exploring from
    ignore_list : list
        List of directories to ignore
    '''

    def __init__(self, root_folder: str, ignore_list: list[str]):
        self.root_folder = root_folder
        self.ignore_list = ignore_list

        # Get the .py files
        self.explore = Explorer(self.root_folder, self.ignore_list)
        self.py_files = self.explore.explore()

        self.entities: list[Entity] = []

        # Parse the entities
        for file in self.py_files:
            entity = Entity(file)
            entity.parse()
            self.entities.append(entity)

    def get_graph(self) -> nx.DiGraph:
        '''
        Method to create a graph based on the entities given. Outputs a
        networkx DiGraph object.
        '''
        nodes = set({})
        edges = set({})

        # Create list of nodes from graph
        for entity in self.entities:
            # Add the file's path as a node
            path = entity.path
            # Split the path into directories
            path = os.path.normpath(path)
            path = path.split(os.sep)
            # Remove the root folder from the path and extension
            root_dir_len = len(os.path.normpath(
                self.root_folder).split(os.sep))
            path = path[root_dir_len:]
            # Transform to python module import format
            path = ".".join(path)
            # Remove the .py extension
            path = path.replace(".py", "")

            nodes.add(path)
            for module in entity.imported_modules:
                nodes.add(module)
                edges.add((path, module))

        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G
