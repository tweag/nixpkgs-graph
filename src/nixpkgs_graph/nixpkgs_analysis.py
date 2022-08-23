from itertools import cycle
import networkx as nx
import json


def general_info(nxG: nx.DiGraph, file_save_path):
    """Generate the basic information of graph.

    Args:
        nxG: A directed nixpkgs graph.

    """

    res = {"name": "general infomation"}

    res["number_of_nodes"] = nxG.number_of_nodes()
    res["number_of_edges"] = nxG.number_of_edges()

    res["citing"] = sorted(nxG.out_degree, key=lambda x: (x[1]))[-10:]

    res["cited"] = sorted(nxG.in_degree, key=lambda x: (x[1]))[-10:]

    sum = 0
    for unit in nxG.out_degree:
        sum = sum + unit[1]
    res["average_dependencies"] = sum / res["number_of_nodes"]

    res["cycles"] = list(nx.simple_cycles(nxG))

    nxG0 = nxG.copy()
    nxG0.remove_nodes_from([i for item in nx.simple_cycles(nxG0) for i in item])
    res["longest_chain_length"] = nx.dag_longest_path_length(nxG0)

    fp = open(file_save_path + "general_info.json", "w")
    print(json.dumps(res), file=fp)
    fp.close()
