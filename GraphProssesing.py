import networkx as nx
import matplotlib.pyplot as plt


def find_highest_deg(G, k=10):
    """
    return k nodes with highest degree
    :param G: the networkx graph
    :param k:
    :return:
    """
    sorted_nodes = sorted(list(G.degree()), key=lambda x: x[1], reverse=True)[:k]
    return [n[0] for n in sorted_nodes]

# def find_central_nodes(G, number=10):


def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.plot(sorted(degrees, reverse=True))
    plt.show()


def multi_to_weighted(G):
    #create empty simple graph
    G_weighted = nx.Graph()
    #copy the nodes from G
    nodes=list(G)
    G_weighted.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            u = nodes[i]
            v = nodes[j]
            ts = []
            if G.get_edge_data(u,v) is None: continue
            for e in G.get_edge_data(u,v):
                ts.append(G.get_edge_data(u, v)[e]['t'])
            G_weighted.add_edge(u, v, weight=len(G.get_edge_data(u,v)), ts=ts)
    return G_weighted





