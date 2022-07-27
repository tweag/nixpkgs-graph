#! /bin/python3

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
filePath = "./rawdata/edges.json"


class Graph:

    def __init__(self):
        self.nxG = nx.DiGraph()  # for display uniquely
        self.label = []

    def addNode(self, i):
        self.nxG.add_node(i)

    def addNodeL(self, i, label):
        self.nxG.add_node(i)
        self.label.append(label)

    def addEdge(self, i, j):
        self.nxG.add_edge(i, j)

    def show(self, xlabel, ylabel, title, arrows, node_size, edge_width):

        self.pos = nx.spring_layout(self.nxG)

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
        # plt.savefig("./rawdata/" + title + ".png")
        plt.show()


data = pd.read_json(filePath)
data.to_csv("./rawdata/edges.csv")
