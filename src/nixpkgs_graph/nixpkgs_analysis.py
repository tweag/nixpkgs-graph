import networkx as nx
import numpy as np


def general_info(nxG: nx.DiGraph):
    """Generate the basic information of graph.
    
    Args:
        nxG: A directed nixpkgs graph.
    
    """
    print(nx.info(nxG))
    nmb_nodes = nxG.number_of_nodes()
    nmb_edges = nxG.number_of_edges()

    print(
        "\nThe largest number of dependencies:\n",
        sorted(nxG.out_degree, key=lambda x: (x[1]))[-10:],
    )
    print("\nThe most cited:\n", sorted(nxG.in_degree, key=lambda x: (x[1]))[-10:])

    sum = 0
    for unit in nxG.out_degree:
        sum = sum + unit[1]
    print("\nThe average number of dependencies:", sum / nmb_nodes)

    print("\nSimple cycles:\n", list(nx.simple_cycles(nxG)))

    nxG0 = nxG.copy()
    nxG0.remove_nodes_from([i for item in nx.simple_cycles(nxG0) for i in item])
    print("\nThe longest path length:", nx.dag_longest_path_length(nxG0))


if __name__ == "__main__":
    nxG = nx.read_gexf("./rawdata/first_graph.gexf")
    general_info(nxG)
