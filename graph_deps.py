from argparse import ArgumentParser

import matplotlib.pyplot as plt
import networkx as nx
from neo4j import GraphDatabase, ManagedTransaction

from src.grapher import Grapher


def create_img_output(graph: nx.DiGraph, scalev: float, scaleh: float, colors=None, width=None):
    plt.figure(figsize=[6*scaleh, 6*scalev])
    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
    if not colors:
        colors = ["black" for _ in graph.edges]
    if not width:
        width = [1 for _ in graph.edges]
    nx.draw(graph, pos, with_labels=True, node_shape="o",
            edge_color=colors, width=width)
    plt.savefig("output_graph.png", bbox_inches='tight', dpi=100)


def create_neo_output(graph: nx.DiGraph, url: str, username: str, password: str):

    def check_node(tx: ManagedTransaction, name: str) -> bool:
        result = tx.run(
            "MATCH (n:Node {name : $name}) RETURN n LIMIT 1", name=name)
        result = result.single()
        return result != None

    def create_node(tx: ManagedTransaction, name: str):
        # Check if node already exists
        exists = check_node(tx, name)
        if not exists:
            result = tx.run(
                "CREATE (n:Node {name : $name}) RETURN n", name=name)
            # Check if node got created
            result = tx.run(
                "MATCH (n:Node {name : $name}) RETURN n LIMIT 1", name=name)
            result = result.single()
            assert result != None
            print(f"Created node {name}")
        else:
            print(f"Node exists {name}")

    def create_edge(tx: ManagedTransaction, node_from: str, node_to: str):
        # Check if nodes exist to create edge
        assert check_node(tx, node_from), "Source node for edge does not exist"
        assert check_node(
            tx, node_to), "Destination node for edge does not exist"
        tx.run("""
               MATCH (nf:Node {name : $node_from})
               MATCH (nt:Node {name : $node_to})
               MERGE (nf)-[r:USES]->(nt)""",
               node_from=node_from, node_to=node_to)
        print(f"Created edge between {node_from} and {node_to}")

    with GraphDatabase.driver(url, auth=(username, password)) as driver:
        driver.verify_connectivity()
        with driver.session() as session:
            for n in graph.nodes:
                session.execute_write(create_node, str(n))
            for e in graph.edges:
                session.execute_write(create_edge, str(e[0]), str(e[1]))
    print("Completed export to Neo4j Database")


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
    ap.add_argument("-e", "--export-type", default="png",
                    help="Type of the export", choices=["png", "neo"])
    ap.add_argument("--neo-url", type=str,
                    help="URL for the Neo4j database")
    ap.add_argument("--neo-username", type=str,
                    help="Username for the Neo4j database")
    ap.add_argument("--neo-password", type=str,
                    help="Password for the Neo4j database")
    args = vars(ap.parse_args())

    root = args["root"]
    ignore_list = args["ignore"]
    scalev = args["scalev"]
    scaleh = args["scaleh"]
    cycle_only = args["cycle_only"]

    export_type = args["export_type"]
    if export_type == "neo":
        neo_url = args["neo_url"]
        neo_username = args["neo_username"]
        neo_password = args["neo_password"]
        assert neo_url is not None, "Neo4j URL is required for Neo4j export"
        assert neo_username is not None, "Neo4j username is required for Neo4j export"
        assert neo_password is not None, "Neo4j password is required for Neo4j export"

    if ignore_list is None:
        ignore_list = []

    grapher = Grapher(root_folder=root, ignore_list=ignore_list)

    graph = grapher.get_graph()
    cycle = None

    try:
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
        if export_type == "neo":
            create_neo_output(cycle_graph, neo_url, neo_username, neo_password)
        else:
            create_img_output(cycle_graph, scalev, scaleh)
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
        if export_type == "neo":
            create_neo_output(graph, neo_url, neo_username, neo_password)
        else:
            create_img_output(graph, scalev, scaleh,
                              colors=colors, width=widths)
