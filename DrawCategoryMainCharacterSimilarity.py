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


###############CATEGORY
G_Cat = nx.read_gpickle('./CategoriesGraph.gpickle')

# largest connected component
components = nx.connected_components(G_Cat)
largest_component = max(components, key=len)
H_Cat = G_Cat.subgraph(largest_component)

# compute community structure
lpc_Cat = nx.community.label_propagation_communities(H_Cat)
community_index_Cat = {n: i for i, com in enumerate(lpc_Cat) for n in com}
max_index = max(community_index_Cat.values())
for community in community_index_Cat:
    print(community_index_Cat[community], community)

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
    if not (n in community_index_Cat.keys()):
        community_index_Cat[n] = 0
"""
# All categories
node_color = [rgb_creator(community_index_Cat[n], max_index) if community_index_Cat[n] != 0 else (0.8, 0.8, 0.8) for n in H]
node_size = [H.degree[node] for node in H.nodes()]
edge_color = [rgb_creator(community_index_Cat[n[0]], max_index) if community_index_Cat[n[0]] == community_index_Cat[n[1]] else (0.8, 0.8, 0.8) for n in nx.edges(H)]
nx.draw_networkx(H, pos=pos, with_labels=False, node_color=node_color, node_size=node_size, edge_color=edge_color, alpha=0.7)
"""
for i in range(67):
    # Fixed category
    node_color = [(0.8, 0.8, 0.8) for n in H]
    node_size = [H.degree[node] for node in H.nodes()]
    edge_color = [(0.8, 0.8, 0.8) for n in nx.edges(H)]
    nx.draw_networkx(H, pos=pos, with_labels=False, node_color=node_color, node_size=node_size, edge_color=edge_color, alpha=0.01)

    # drama=[9,18,19,34,35,36,45,48,50,55,56,57] # fiction=[2,3,4,6,7,8,10,11,13,16,17,18,22,24,25,27,28,29,30,32,33,34,35,41,44,47,50,65,67]
    # biography=[12,35,36,48,60,61,64,66] # poetry=[5,21,26,27,37,38,50,53,54] # history=[5,9,11,12,14,16,18,27,29,30,32,34,35,36,40,41,50,60,61,63,67]
    sub_list = [n for n in H if community_index_Cat[n] in [i]]
    H_Category = H.subgraph(sub_list)
    node_color = [rgb_creator(community_index_Cat[n], max_index) for n in H_Category]
    node_size = [H_Category.degree[node] for node in H_Category.nodes()]
    # edge_color = [rgb_creator(community_index_Cat[n[0]], max_index) for n in nx.edges(H_Category)]
    edge_color = [rgb_creator(community_index_Cat[n[0]], max_index) if community_index_Cat[n[0]] == community_index_Cat[n[1]] else (0.8, 0.8, 0.8) for n in nx.edges(H_Category)]
    nx.draw_networkx(H_Category, pos=pos, with_labels=False, node_color=node_color, node_size=node_size, edge_color=edge_color, alpha=0.9)


    # Title
    font = {"color": "k", "fontweight": "bold", "fontsize": 20}
    ax.set_title(i, font)
    # Legend
    font["color"] = "r"
    ax.text(0.80, 0.10, "node color = category or community", horizontalalignment="center", transform=ax.transAxes, fontdict=font,)
    ax.text(0.80, 0.06, "node size = degree", horizontalalignment="center", transform=ax.transAxes, fontdict=font,)

    # Resize figure for label readability
    ax.margins(0.1, 0.05)
    fig.tight_layout()
    plt.axis("off")
    plt.show()
