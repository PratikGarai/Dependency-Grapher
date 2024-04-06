import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from src.grapher import Grapher

if __name__ == "__main__":
    root = "sample"
    ignore_list = ["ignore"]

    grapher = Grapher(root_folder=root, ignore_list=ignore_list)

    graph = grapher.get_graph()
    pos = graphviz_layout(graph, prog="dot")
    nx.draw(graph, pos, with_labels=True, node_shape="o")
    plt.savefig("image.png",bbox_inches='tight',dpi=100)
