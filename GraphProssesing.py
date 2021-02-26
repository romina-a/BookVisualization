import networkx as nx
import matplotlib.pyplot as plt


# TODO add function descriptions
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
    """
    plots degree distribution of G
    :param G: nx
    """
    degrees = [n[1] for n in find_highest_deg(G)]
    plt.plot(sorted(degrees, reverse=True))
    plt.show()


def find_highest_pagerank(G,  k='all'):
    """
    return k nodes with highest pagerank if k is
    :param G: nx.MultiGraph the networkx graph
    :param k: int
    :return: sorted list of tuples of the form (<node_id>, <node_pagerank>)
    """
    if k == 'all':
        k = len(list(G))
    ranks = nx.pagerank_numpy(G)
    sorted_nodes = sorted(ranks.items(), key=lambda x:x[1], reverse=True)[:k]
    return sorted_nodes


def plot_pagerank_dist(G):
    degrees = [n[1] for n in find_highest_pagerank(G)]
    plt.plot(sorted(degrees, reverse=True))
    plt.show()








