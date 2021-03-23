import GraphProssesing
import networkx as nx
import os


def topk_pagerank_history(G, num_of_snapshots, k):
    topk = GraphProssesing.find_highest_pagerank(G, k=k)
    history = []
    for char in topk:
        history = GraphProssesing.pagerank_history_for_character(G, char[0], num_of_snapshots)
    return history


def normalization(history, k=1):
    normalized_history = []
    for rank in history:
        if rank <= max(history)/5:
            normalized_history.append(1)
        elif rank > max(history)/5 and rank <= 2*max(history)/5:
            normalized_history.append(2)
        elif rank > 2*max(history)/5 and rank <= 3*max(history)/5:
            normalized_history.append(3)
        elif rank > 3*max(history)/5 and rank <= 4*max(history)/5:
            normalized_history.append(4)
        elif rank > 4*max(history)/5:
            normalized_history.append(5)
    return normalized_history


def comparison(history1, history2, k=1):
    s = 0
    for i in range(min(len(history1), len(history2))):
        s += abs(history1[i] - history2[i])
    if min(len(history1), len(history2)) == 0:
        return 0
    else:
        return 1-s/(4*min(len(history1), len(history2)))


G = nx.Graph()

addresses = os.listdir("./SavedGraph/")
for address in addresses:
    name = address.split("___")[1][:-8]
    G.add_node(name)

list = []
count = 0
for address in addresses:
    G1 = nx.read_gpickle("./SavedGraph/" + address)
    name = address.split("___")[1][:-8]
    print(count, name)
    list.append([name, normalization(topk_pagerank_history(G1, 15, 1))])
    count += 1

for x in range(len(list)):
    for y in range(len(list)):
        if list[x][0] != list[y][0] and not (G.has_edge(list[x][0], list[y][0])) and comparison(list[x][1], list[y][1]) > 0.8:
            G.add_edge(list[x][0], list[y][0])

nx.write_gpickle(G, './SimilarityGraph.gpickle')
