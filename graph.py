#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: [ ps.matplotlib ps.networkx ps.pandas ps.scipy])"

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
# we will also need scipy because it's used by networkx

filePath = "./rawdata/edges.json"


class Graph:

    def __init__(self):
        self.nxG = nx.DiGraph()  # Directed Graph
        self.label = []

    def addNode(self, i):
        self.nxG.add_node(i)

    def addNodeL(self, i, label):
        self.nxG.add_node(i)
        self.label.append(label)

    def addEdge(self, i, j):
        self.nxG.add_edge(i, j)

    def show(self, xlabel, ylabel, title, arrows, node_size, edge_width):

        # self.pos = nx.spring_layout(self.nxG)
        self.pos = nx.random_layout(self.nxG)

        if len(self.label) == 0:
            self.label = [0 for i in range(0, len(self.nxG.nodes))]
        plt.figure()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        nx.draw_networkx_nodes(self.nxG, pos=self.pos, node_size=node_size, node_color=self.label,
                               cmap=plt.get_cmap("viridis"))
        nx.draw_networkx_edges(self.nxG, pos=self.pos,
                               arrows=arrows, width=edge_width)
        plt.savefig("./rawdata/" + title + ".png")
        # plt.show()

# 1. Pre-processing of data


data = pd.read_json(filePath)

# Change the order of the columns
order = ["name", "pname", "version", "package", "buildInputs"]
data = data[order]


# The splitBuild function is used to cut the buildInputs and extract the package name from the full address with a hash string.
def splitBuild(x):

    # Some packages fails to evaluate their buildInputs so we may get "False".
    if type(x) == bool:
        return []

    list = x.split(" ")

    # The last one is always " ", so we need to remove it
    del list[-1]

    res = []
    for input in list:
        if input[-4:] == "-dev":
            res.append(input[44: -4])
        else:
            res.append(input[44:])
    return res


data["buildInputs"] = data.buildInputs.apply(splitBuild)


# the dict for package sets like python3Packages, we will use it for color
packages = {"nixpkgs"}


def getPackages(x):
    if len(x) <= 2:
        return  # package directly under nixpkgs
    packages.add(x[1])


data.package.apply(getPackages)
packages = list(packages)


def colorPackages(x):
    if len(x) <= 2:
        return 1
    else:
        return packages.index(x[1])+1


data["group"] = data.package.apply(colorPackages)


# 2. Add nodes

g = Graph()


def addNode(x):
    # For now we can't use x.group as label because somes edges will refer to somes points without color
    g.addNode(x.name)


data.apply(addNode, axis=1)  # axis = 1 means we do it row by row
# print(len(g.nxG))


# 3. Add edges

def addEdge(x):
    source = x.name
    for target in x.buildInputs:
        g.addEdge(source, target)


data.apply(addEdge, axis=1)


# 4. Show graph

g.show(xlabel="x", ylabel="y", title="First graph",
       arrows=False, node_size=0.1, edge_width=0.03)

print(data)

# 5. Final output
data.to_csv("./rawdata/edges.csv")
