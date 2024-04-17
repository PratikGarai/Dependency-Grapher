from argparse import ArgumentParser

import matplotlib.pyplot as plt
import networkx as nx

from src.grapher import Grapher


def create_output(graph: nx.DiGraph, scalev: float, scaleh: float, colors=None, width=None):
    plt.figure(figsize=[6*scaleh, 6*scalev])
    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
    if not colors:
        colors = ["black" for _ in graph.edges]
    if not width:
        width = [1 for _ in graph.edges]
    nx.draw(graph, pos, with_labels=True, node_shape="o", edge_color=colors, width=width)
    plt.savefig("output_graph.png", bbox_inches='tight', dpi=100)


if __name__ == "__main__":

    ap = ArgumentParser()
    ap.add_argument("-r", "--root", required=True,
                    help="Root folder to start exploring from")
    ap.add_argument("-i", "--ignore", nargs="+",
                    help="List of directories to ignore")
    ap.add_argument("-sv", "--scalev", type=float, default=1.0,
                    help="Vertical sale of the graph")
    ap.add_argument("-sh", "--scaleh", type=float, default=1.0,
                    help="Horizontal sale of the graph")
    ap.add_argument("-c", "--cycle_only", action="store_true",
                    help="Show only the cycles")
    args = vars(ap.parse_args())

    root = args["root"]
    ignore_list = args["ignore"]
    scalev = args["scalev"]
    scaleh = args["scaleh"]
    cycle_only = args["cycle_only"]

    if ignore_list is None:
        ignore_list = []

    grapher = Grapher(root_folder=root, ignore_list=ignore_list)

    graph = grapher.get_graph()
    cycle = None

    try :
        cycle = nx.find_cycle(graph, orientation="original")
    except nx.NetworkXNoCycle:
        print("No cycle found")

    if cycle_only:
        if cycle is None:
            print("Exiting as no cycle found")
            exit(0)
        cycle_graph = nx.DiGraph()
        for edge in cycle:
            cycle_graph.add_edge(edge[0], edge[1])
        create_output(cycle_graph, scalev, scaleh)
    else:
        colors = None
        widths = None
        if cycle is not None:
            edge_set = set()
            for edge in cycle:
                edge_set.add((edge[0], edge[1]))
            print("Cycle found")
            for edge in graph.edges:
                if edge in edge_set:
                    graph.edges[edge]["color"] = "red"
                    graph.edges[edge]["penwidth"] = 2
                else:
                    graph.edges[edge]["color"] = "black"
                    graph.edges[edge]["penwidth"] = 1
            colors = nx.get_edge_attributes(graph, "color").values()
            widths = list(nx.get_edge_attributes(graph, "penwidth").values())
        create_output(graph, scalev, scaleh, colors=colors, width=widths)
