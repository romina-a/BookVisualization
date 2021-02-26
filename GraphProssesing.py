import networkx as nx
import matplotlib.pyplot as plt


def find_highest_deg(G, k=-1):
    """
    return k nodes with highest degree if k is -1, returns all degrees
    :param G: the networkx graph
    :param k:
    :return: sorted list of tuples of the form (<node_id>, <node_degree>)
    """
    if k == -1:
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


def find_highest_pagerank(G, k=-1):
    """
    return k nodes with highest pagerank if k is -1, returns all pageranks
    :param G: nx.MultiGraph the networkx graph
    :param k: int
    :return: sorted list of tuples of the form (<node_id>, <node_pagerank>)
    """
    if k == -1:
        k = len(list(G))
    ranks = nx.pagerank_numpy(G)
    sorted_nodes = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:k]
    return sorted_nodes


# TODO: is pagerank distribution a thing?
def plot_pagerank_dist(G):
    """
    plots pagerank distribution of G
    :param G: nx
    """
    degrees = [n[1] for n in find_highest_pagerank(G)]
    plt.plot(sorted(degrees, reverse=True))
    plt.show()


# TODO: do we need 'count' snapshot?
def create_snapshot(G, t1, t2):
    snapshot = nx.create_empty_copy(G, with_data=True)
    selected_edges = [e for e in G.edges(data=True) if e[2]['time'] in range(t1, t2)]
    snapshot.add_edges_from(selected_edges)
    return snapshot


def pagerank_history_for_character(G, character_name, num_of_snapshots):
    end = G.graph['end_time']
    step = max(end // (num_of_snapshots - 1), 1)
    pagerank_history = []
    for i in range(0, end, step):
        snap = create_snapshot(G, i, i + step)
        pageranks = find_highest_pagerank(snap)
        pagerank_history.append(dict(pageranks)[character_name])
    return pagerank_history


def draw_pagerank_by_time_for_character(G, character_name, num_of_snapshots):
    pagerank_history = pagerank_history_for_character(G, character_name, num_of_snapshots)
    plt.plot(pagerank_history)
    plt.show()


def top5_pagerank_history(G, num_of_snapshots):
    top5 = find_highest_pagerank(G, k=5)
    for char in top5:
        history = pagerank_history_for_character(G, char[0], num_of_snapshots)
        plt.plot(history, label=char[0] + "-overall page rank:{0:6.2f}".format(char[1]))
        plt.ylabel('Page Rank')
        plt.xlabel('time')
    plt.legend()
    plt.show()


# def multi_to_weighted(G):
#     """
#     returns an nx.Graph, equal to the input MultiGraph,
#     with the following properties:
#             node attributes: the same as node attributes of the input graph G
#             edge attributes: 'weight': total #times nodes u and v appeared closer than max_dist lines
#                              'times': list of time stamps for each time u and v appeared closer than max_dist
#                                       length of the list = weight
#
#     :param G: nx.MultiGraph, edges must have 'time' attribute
#     :return: Weighted nx.Graph
#     """
#     # create empty simple graph
#     G_weighted = nx.Graph()
#     # copy the nodes from G
#     nodes_info = list(G.nodes(data=True))
#     nodes = list(G)
#     G_weighted.add_nodes_from(nodes_info)
#     for i in range(len(nodes)):
#         for j in range(i + 1, len(nodes)):
#             u = nodes[i]
#             v = nodes[j]
#             ts = []
#             if G.get_edge_data(u, v) is None: continue
#             for e in G.get_edge_data(u, v):
#                 ts.append(G.get_edge_data(u, v)[e]['time'])
#             G_weighted.add_edge(u, v, weight=len(G.get_edge_data(u, v)), times=ts)
#     return G_weighted



