import networkx as nx
import os

G = nx.Graph()
list = []
addresses = os.listdir("./SavedGraph/")
for address in addresses:
    name = address.split("___")[1][:-8]
    author = address.split("___")[0]
    G.add_node(name)
    list.append([name, author])
    print(name, author)

for x in range(len(list)):
    for y in range(len(list)):
        if list[x][1] == list[y][1] and list[x][0] != list[y][0] and not G.has_edge(list[x][0], list[y][0]):
            G.add_edge(list[x][0], list[y][0])

nx.write_gpickle(G, './AuthorGraph.gpickle')
