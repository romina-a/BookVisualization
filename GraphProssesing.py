import networkx as nx
import matplotlib.pyplot as plt


def find_highest_deg(G, number=10):
    sorted_nodes = sorted(list(G.degree()), key=lambda x: x[1], reverse=True)[:number]
    return [n[0] for n in sorted_nodes]


def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.plot(sorted(degrees, reverse=True))
    plt.show()


