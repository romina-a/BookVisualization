# based on a code from https://www.inetbio.org/wormnet/downloadnetwork.php
import networkx as nx
import matplotlib.pyplot as plt


def rgb_creator(index, max_index):
    if (index/max_index) < 0.33:
        r = 1 - abs(index-max_index/6)/(max_index/6)*0.67
        g = index/max_index
        b = 0
    elif 0.33 <= (index / max_index) <= 0.67:
        r = 0.67 - index/max_index
        g = 1 - abs(index-3*max_index/6)/(max_index/6)*0.67
        b = index/max_index - 0.33
    else:
        r = 0
        g = 1 - index/max_index
        b = 1 - abs(index-5*max_index/6)/(max_index/6)*0.67
    color = (r, g, b)
    return color


###############Author
G_Aut = nx.read_gpickle('./AuthorGraph.gpickle')

# compute community structure
lpc_Aut = nx.community.label_propagation_communities(G_Aut)
community_index_Aut = {n: i for i, com in enumerate(lpc_Aut) for n in com}
max_index = max(community_index_Aut.values())
for community in community_index_Aut:
    print(community_index_Aut[community], community)


###############SIMILARITY
G_Sim = nx.read_gpickle('./SimilarityGraph.gpickle')

# largest connected component
components = nx.connected_components(G_Sim)
largest_component = max(components, key=len)
H = G_Sim.subgraph(largest_component)


###############DRAW GRAPH
fig, ax = plt.subplots(figsize=(20, 15))
pos = nx.spring_layout(H, k=0.15, seed=3040)
for n in H:
    if not (n in community_index_Aut.keys()):
        community_index_Aut[n] = 0

node_color = [(0.8, 0.8, 0.8) for n in H]
node_size = [H.degree[node] for node in H.nodes()]
edge_color = [(0.8, 0.8, 0.8) for n in nx.edges(H)]
nx.draw_networkx(H, pos=pos, with_labels=False, node_color=node_color, node_size=node_size, edge_color=edge_color, alpha=0.01)

# Author number
sub_list = [n for n in H if community_index_Aut[n] == 127]
H_Author = H.subgraph(sub_list)
node_color = [rgb_creator(community_index_Aut[n], max_index) for n in H_Author]
node_size = [H_Author.degree[node] for node in H_Author.nodes()]
edge_color = [rgb_creator(community_index_Aut[n[0]], max_index) for n in nx.edges(H_Author)]
nx.draw_networkx(H_Author, pos=pos, with_labels=False, node_color=node_color, node_size=node_size, edge_color=edge_color, alpha=0.9)

# Title
font = {"color": "k", "fontweight": "bold", "fontsize": 20}
ax.set_title("Book Category Network", font)
# Legend
font["color"] = "r"
ax.text(0.80, 0.10, "node color = category or community", horizontalalignment="center", transform=ax.transAxes, fontdict=font,)
ax.text(0.80, 0.06, "node size = degree", horizontalalignment="center", transform=ax.transAxes, fontdict=font,)

# Resize figure for label readability
ax.margins(0.1, 0.05)
fig.tight_layout()
plt.axis("off")
plt.show()
