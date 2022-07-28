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

    def addEdge(self, i, j):
        self.nxG.add_edge(i, j)

    def show(self, xlabel, ylabel, title, arrows, node_size, edge_width):

        self.pos = nx.spring_layout(self.nxG)
        # self.pos = nx.random_layout(self.nxG)

        self.label = [g.nxG.nodes[node]["group"] for node in g.nxG]

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

# Read json file
data = pd.read_json(filePath).head(10000)

# Remove repeated nodes
data.drop_duplicates(subset=["name", "pname", "version"], keep='first',
                     inplace=True, ignore_index=True)

# Change the order of the columns
order = ["name", "pname", "version", "package", "buildInputs"]
data = data[order]
data.rename(columns={"name": "Id"}, inplace=True)


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
            res.append(input[44: -4])
        else:
            res.append(input[44:])
    return res


data["buildInputs"] = data.buildInputs.apply(splitBuild)


# The dict for package sets like python3Packages, we will use it for color
packages = {"nixpkgs"}


def getPackages(x):
    if len(x) <= 2:
        return  # package directly under nixpkgs
    packages.add(x[1])


data.package.apply(getPackages)
packages = list(packages)


def setGroup(x):
    if len(x) <= 2:
        return 1
    else:
        return packages.index(x[1]) + 1


data["group"] = data.package.apply(setGroup)


# 2. Add nodes

g = Graph()


def addNode(x):
    g.nxG.add_node(x.Id, group=x.group)


data.apply(addNode, axis=1)  # axis = 1 means we do it row by row


# 3. Add edges

def addEdge(x):
    source = x.Id
    for target in x.buildInputs:
        g.addEdge(source, target)


data.apply(addEdge, axis=1)


# 4 Complete the "group" data

# Since we have not evaluated all the nodes successfully, all the targets involved in some edges are not in the node list.
# But they are still added to the graph, so we need to add group attribute for them.
for node, attrs in g.nxG.nodes(data=True):
    if "group" not in attrs:
        g.nxG.add_node(node, group=0)


# 5. Show graph

print("number of nodes:", g.nxG.number_of_nodes())
print("number of edges:", g.nxG.number_of_edges())

g.show(xlabel="x", ylabel="y", title="First graph",
       arrows=False, node_size=0.1, edge_width=0.01)


# 6. Final output
data.to_csv("./rawdata/edges.csv")
