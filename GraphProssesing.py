import networkx as nx
import matplotlib.pyplot as plt
import DrawGraph
import numpy as np

PAGERANK_THRESHOLD_DEFAULT = 0.5


# TODO: remove the nodes that appear once with small time stamp/low degree (metadata)
#  e.g.: Shakespeare


def create_snapshot(G, t1, t2):
    """
    Returns an nx.multiGraph (snapshot) that is a subset of the graph G:
            The snapshot contains all nodes
                and the edges that appeared within t1 and t2 time span:
            The graph attributes are preserved.
            All the nodes and node attributes are preserved.
            All edges with t1<='time'<t2 are contained in snapshot.
            All other edges are removed.

    :param G: nx.MultiGraph, attributes used:
                                    -edge attributes: 'time'
    :param t1: int, minimum edge 'time' to include.
    :param t2: int, maximum edge 'time' to include. The last 'time'=t2-1
    :return: nx.MultiGraph, the snapshot, attributes are the same as G
    """
    snapshot = nx.create_empty_copy(G, with_data=True)
    for (node, data) in snapshot.nodes(data=True):
        data['times'] = [i for i in data['times'] if i in range(t1, t2)]
        data['count'] = len(data['times'])
    selected_edges = [e for e in G.edges(data=True) if e[2]['time'] in range(t1, t2)]
    snapshot.add_edges_from(selected_edges)
    return snapshot


# ~~~~~~~~~~~~~~~~~ Single Graph ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_highest_deg(G, k=-1):
    """
    Returns k nodes with highest degree.
    If k is -1, returns all degrees.

    :param G: nx.MultiGraph
    :param k: int
    :return: sorted list of k tuples of the form (<node_id>, <node_degree>)
    """
    if k == -1:
        k = len(list(G))
    sorted_nodes = sorted(list(G.degree()), key=lambda x: x[1], reverse=True)[:k]
    return sorted_nodes


def find_highest_pagerank(G, k=-1):
    """
    Returns k nodes with highest pagerank.
    If k is -1, returns all pageranks.

    :param G: nx.MultiGraph
    :param k: int
    :return: sorted list of k tuples of the form (<node_id>, <node_pagerank>)
    """
    if k == -1:
        k = len(list(G))
    ranks = nx.pagerank_numpy(G)
    sorted_nodes = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:k]
    return sorted_nodes


def find_central_characters(G, page_rank_threshold=PAGERANK_THRESHOLD_DEFAULT):
    """
    returns list: [(<name>,<pagerank>),...] for the central part
    :param G:
    :param page_rank_threshold:
    :return:
    """
    A = find_highest_pagerank(G)
    sum = 0
    B = []
    for i in A:
        B.append(i)
        sum += i[1]
        if sum > page_rank_threshold: break
    return B


def find_highest_count(G, k=-1):
    """
    Returns k nodes with highest count.
    If k is -1, returns all degrees.

    :param G: nx.MultiGraph
    :param k: int
    :return: sorted list of k tuples of the form (<node_id>, <count>)
    """
    if k == -1:
        k = len(list(G))
    nodes = [(i, G.nodes(data=True)[i]['count']) for i in list(G)]
    sorted_nodes = sorted(nodes, key=lambda x: x[1], reverse=True)[:k]
    return sorted_nodes


# ~~~~~~~~~~~~~~~~~ Time series ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TODO: add x values based on the step size
def pagerank_history_for_character(G, character_name, num_of_snapshots):
    """
    1. Creates num_of_snapshots equally distanced snapshots between 0 and 'end_time'.
    2. Calculates page rank for all characters in each snapshot
    3. Returns pagerank_history: a list of the node <character_name>'s pagerank
            in each snap shot. len(pagerank_history) = num_of_snapshots

    :param G: nx.MultiGraph, attributes used:
                                -graph attributes: 'end_time'
                                -edge attributes: 'time'
    :param character_name: string, must be a node id in G
    :param num_of_snapshots: int, the number of equally distanced snapshots.
    :return: list of float, <character_name>'s pagerank history
    """
    end = G.graph['end_time']
    step = max(end // (num_of_snapshots), 1)
    pagerank_history = []
    for i in range(0, end, step):
        snap = create_snapshot(G, i, i + step)
        pageranks = find_highest_pagerank(snap)
        pagerank_history.append(dict(pageranks)[character_name])
    return pagerank_history


def count_history_for_character(G, character_name, num_of_snapshots):
    """
    1. Creates num_of_snapshots equally distanced snapshots between 0 and 'end_time'.
    2. Returns count_history: a list of the node <character_name>'s count
            in each snap shot. len(count_history) = num_of_snapshots

    :param G: nx.MultiGraph, attributes used:
                                -graph attributes: 'end_time'
                                -edge attributes: 'time'
                                -node attributes: 'count'
    :param character_name: string, must be a node id in G
    :param num_of_snapshots: int, the number of equally distanced snapshots.
    :return: list of int, <character_name>'s count history
    """
    end = G.graph['end_time']
    step = max(end // (num_of_snapshots), 1)
    count_history = []
    for i in range(0, end, step):
        snap = create_snapshot(G, i, i + step)
        count_history.append(snap.nodes(data=True)[character_name]['count'])
    return count_history


def central_characters_through_time(G, num_of_snapshots, pagerank_threshold=PAGERANK_THRESHOLD_DEFAULT):
    """
    returns k most important characters in each snapshots

    :param G:
    :param num_of_snapshots:
    :param pagerank_threshold:
    :return: list of #num_of_snapshots sets of tuples (<name>,<pagerank>)
    """
    end = G.graph['end_time']
    step = max(end // num_of_snapshots, 1)
    importants = []
    for i in range(0, end, step):
        snap = create_snapshot(G, i, i + step)
        importants.append(set(find_central_characters(snap, pagerank_threshold)))
    return importants


def degmorethanone_characters_through_time(G, num_of_snapshots):
    """
    returns k most important characters in each snapshots

    :param G:
    :param num_of_snapshots:
    :return: list of #num_of_snapshots sets of tuples (<name>,<deg>)
    """
    end = G.graph['end_time']
    step = max(end // num_of_snapshots, 1)
    importants = []
    for i in range(0, end, step):
        snap = create_snapshot(G, i, i + step)
        importants.append(set([(n, snap.degree[n]) for n in list(snap) if snap.degree[n] > 0]))
    return importants


# ~~~~~~~~~~~~~~~~~ Plots ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def plot_degree_dist(G, loglog=True, title="", save_adr=""):
    """
    plots degree distribution of G

    :param G: nx.MultiGraph
    """
    degree_hist = nx.degree_histogram(G)
    degree_hist = list(zip([i for i in range(len(degree_hist))], degree_hist))
    degree_hist = dict([i for i in degree_hist if i[1] > 0 and i[0] > 0])
    x = list(degree_hist.keys())
    y = list(degree_hist.values())
    if loglog is True:
        x = np.log10(x)
        y = np.log10(y)
    plt.scatter(x=x, y=y, marker='.')
    plt.xlabel("degree")
    plt.ylabel("frequency")
    plt.title(title)
    if save_adr != "":
        plt.savefig(save_adr)
    plt.show()


def plot_pageranks(G, loglog=True):
    impts = find_highest_pagerank(G)
    x = [i for i in range(len(impts))]
    y = list(dict(impts).values())
    if loglog:
        y = np.log(y)
        x = np.log(x)
    plt.scatter(x=x, y=y)
    plt.show()


# ~~~~~~~~~~~~~~~~~ Plots by time ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def plot_pagerank_by_time_for_character(G, character_name, num_of_snapshots):
    pagerank_history = pagerank_history_for_character(G, character_name, num_of_snapshots)
    plt.plot(pagerank_history)
    plt.show()


def plot_count_by_time_for_character(G, character_name, num_of_snapshots):
    pagerank_history = count_history_for_character(G, character_name, num_of_snapshots)
    plt.plot(pagerank_history)
    plt.show()


def plot_topk_pagerank_history(G, num_of_snapshots, k):
    """
    returns topk most important characters and plots their pagerank through time
    :param G:
    :param num_of_snapshots:
    :param k:
    :return:
    """
    topk = find_highest_pagerank(G, k=k)
    for char in topk:
        history = pagerank_history_for_character(G, char[0], num_of_snapshots)
        plt.plot(history, label=char[0] + "-overall page rank:{0:6.2f}".format(char[1]))
        plt.ylabel('Page Rank')
        plt.xlabel('time')
    plt.legend()
    plt.show()


def plot_fluidity_total(G, num_of_snapshots, save_adr=""):
    imp = degmorethanone_characters_through_time(G, num_of_snapshots)
    change = []
    prevs = set()
    for s in imp:
        curs = set([i[0] for i in s])
        change.append(len(curs ^ prevs))
        prevs = curs
    plt.plot(change)
    plt.ylabel('change')
    plt.xlabel('time')
    if save_adr != "":
        plt.savefig(save_adr)
    plt.show()
    return change


def plot_fluidity_central(G, num_of_snapshots,
                          pagerank_threshold=PAGERANK_THRESHOLD_DEFAULT,
                          save_adr=""):
    imp = central_characters_through_time(G, num_of_snapshots,
                                          pagerank_threshold=pagerank_threshold)
    change = []
    prevs = set()
    for s in imp:
        curs = set([i[0] for i in s])
        change.append(len(curs ^ prevs))
        prevs = curs
    plt.plot(change)
    plt.ylabel('change')
    plt.xlabel('time')
    if save_adr != "":
        plt.savefig(save_adr)
    plt.show()
    return change


# ~~~~~~~~~~~~~~~ Graph Drawing ~~~~~~~~~~~~~~~~~~~~~~~~~~
def draw_graph_through_time(G, num_of_snapshots, pagerank_threshold=0.5):
    """
    Creates and saves snap shots for the central part of the graph
    (if pagerank_threshold is 1, gives the whole graph)
    :param G:
    :param num_of_snapshots:
    :param pagerank_threshold:
    :return:
    """
    end = G.graph['end_time']
    step = max(end // num_of_snapshots, 1)
    importants = set()
    snaps = []
    for i in range(0, end, step):
        snap = create_snapshot(G, i, i + step)
        snaps.append(snap)
        importants = importants.union(set(dict(find_central_characters(snap, pagerank_threshold))))
    for i, snap in enumerate(snaps):
        DrawGraph.draw_graph_plotly(snap.subgraph(importants),
                                    save_adr=f"./graph{i + 1}.png", show=False)


# ~~~~~~~~~~~~~~~~ information already in graph ~~~~~~~~~~~~~~~~~~~~~~~
def print_merged_nodes(G):
    print("merged nodes:")
    for i in list(G):
        if "contraction" in G.nodes[i]:
            print(f'{i}\t{list(G.nodes[i]["contraction"].keys())}')
    print()

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
