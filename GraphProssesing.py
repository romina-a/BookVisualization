import networkx as nx
import matplotlib.pyplot as plt

# TODO make readable
def find_highest_deg(G, k='all'):
    """
    return k nodes with highest degree
    :param G: the networkx graph
    :param k:
    :return: sorted list of tuples of the form (<node_id>, <node_degree>)
    """
    if k == 'all':
        k = len(list(G))
    sorted_nodes = sorted(list(G.degree()), key=lambda x: x[1], reverse=True)[:k]
    return sorted_nodes


def plot_degree_dist(G):
    degrees = [n[1] for n in find_highest_deg(G)]
    plt.plot(sorted(degrees, reverse=True))
    plt.show()


def find_highest_pagerank(G,  k='all'):
    if k == 'all':
        k = len(list(G))
    ranks = nx.pagerank_numpy(G)
    sorted_nodes = sorted(ranks.items(), key=lambda x:x[1], reverse=True)[:k]
    return sorted_nodes


def plot_pagerank_dist(G):
    degrees = [n[1] for n in find_highest_pagerank(G)]
    plt.plot(sorted(degrees, reverse=True))
    plt.show()


def multi_to_weighted(G, time_stamp='time'):
    #create empty simple graph
    G_weighted = nx.Graph()
    #copy the nodes from G
    nodes_info = list(G.nodes(data=True))
    nodes = list(G)
    G_weighted.add_nodes_from(nodes_info)
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            u = nodes[i]
            v = nodes[j]
            ts = []
            if G.get_edge_data(u, v) is None: continue
            for e in G.get_edge_data(u, v):
                ts.append(G.get_edge_data(u, v)[e][time_stamp])
            G_weighted.add_edge(u, v, weight=len(G.get_edge_data(u, v)), times=ts)
    return G_weighted








