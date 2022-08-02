import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import os

# we will also need scipy because it's used by networkx


# The Integrated Functions
def graph(title="first_graph", arrows=False, node_size=0.1, edge_width=0.01):
    filePath = os.getcwd() + "/rawdata/nodes.json"
    # Read json file
    data = pd.read_json(filePath)
    # Create Graph
    g = Graph()

    data = preProcess(data)
    addNodes(data, g)
    addEdges(data, g)
    completeData(g)
    showGraph(g, title, arrows, node_size, edge_width)
    toCsv(data)


class Graph:
    def __init__(self):
        self.nxG = nx.DiGraph()  # Directed Graph
        self.label = []

    def addEdge(self, i, j):
        self.nxG.add_edge(i, j)

    def show(self, xlabel, ylabel, title, arrows, node_size, edge_width):

        # self.pos = nx.spring_layout(self.nxG)
        self.pos = nx.random_layout(self.nxG)

        self.label = [self.nxG.nodes[node]["group_id"] for node in self.nxG]

        # width then length, unit: 100 pixels
        plt.figure(figsize=(10, 10), dpi=300)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        nx.draw_networkx_nodes(
            self.nxG,
            pos=self.pos,
            node_size=node_size,
            node_color=self.label,
            cmap=plt.get_cmap("viridis"),
        )
        nx.draw_networkx_edges(self.nxG, pos=self.pos, arrows=arrows, width=edge_width)
        plt.savefig("./rawdata/" + title + ".png")
        # plt.show()


# 1. Pre-processing of _data


def preProcess(_data):
    # Remove repeated nodes
    _data.drop_duplicates(
        subset=["id", "pname", "version"], keep="first", inplace=True, ignore_index=True
    )
    # Change the order of the columns
    order = ["id", "pname", "version", "package", "buildInputs"]
    _data = _data[order]
    # Split buildInputs
    df = _data.copy()
    df["buildInputs"] = df["buildInputs"].apply(splitBuild)
    # Generat group attribute
    generateGroup(df)
    return df


def splitBuild(x):
    # The splitBuild function is used to cut the buildInputs and extract the package name from the full address with a hash string.
    # Some packages fails to evaluate their buildInputs so we may get "False".
    if type(x) == bool:
        return []

    list = x.split(" ")

    # The last one is always " ", so we need to remove it
    del list[-1]

    res = []
    for input in list:
        if input[-4:] == "-dev":
            res.append(input[44:-4])
        else:
            res.append(input[44:])
    return res


def generateGroup(_data):
    _data["group"] = _data["package"].map(lambda x: x[1] if len(x) >= 3 else np.nan)
    _data["group_id"] = _data["group"].map(_data["group"].unique().tolist().index)


# 2. Add nodes


def addNodes(_data, _g):
    _data.apply(addNode, _g=_g, axis=1)  # axis = 1 means we do it row by row


def addNode(x, _g):
    _g.nxG.add_node(
        x.id, pname=x.pname, version=x.version, group=x.group, group_id=x.group_id
    )


# 3. Add edges


def addEdges(_data, _g):
    _data.apply(addEdge, _g=_g, axis=1)


def addEdge(x, _g):
    source = x.id
    for target in x.buildInputs:
        _g.addEdge(source, target)


# 4 Complete data

# Since we have not evaluated all the nodes successfully, all the targets involved in some edges are not in the node list.
# But they are still added to the graph, so we need to add group attribute for them.
def completeData(_g):
    for node, attrs in _g.nxG.nodes(data=True):
        if "group_id" not in attrs:
            _g.nxG.add_node(node, group_id=0)


# 5. Show graph


def showGraph(_g, _title, _arrows, _node_size, _edge_width):
    print("number of nodes:", _g.nxG.number_of_nodes())
    print("number of edges:", _g.nxG.number_of_edges())
    _g.show(
        xlabel="x",
        ylabel="y",
        title=_title,
        arrows=_arrows,
        node_size=_node_size,
        edge_width=_edge_width,
    )


# 6. Final output
def toCsv(_data):
    _data.to_csv("./rawdata/nodes.csv")


if __name__ == "__main__":
    graph()
