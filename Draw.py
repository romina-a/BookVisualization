import networkx as nx
import matplotlib.pyplot as plt

# G = nx.read_gpickle("./CategoriesGraph.gpickle")
# G = nx.read_gpickle('./SimilarityGraph.gpickle')
# G = nx.read_gpickle("./AuthorGraph.gpickle")
G = nx.read_gpickle("./YearGraph.gpickle")

"""
plt.figure(figsize=(20, 15))
nx.draw(G, pos=nx.spring_layout(G, k=0.07), node_size=[G.degree[n] for n in G], node_color="blue", with_labels=False)
plt.show()
"""

# largest connected component
components = nx.connected_components(G)
largest_component = max(components, key=len)
H = G.subgraph(largest_component)

# compute community structure
lpc = nx.community.label_propagation_communities(H)
community_index = {n: i for i, com in enumerate(lpc) for n in com}

for community in community_index:
    print(community_index[community], community)

"""
fig, ax = plt.subplots(figsize=(20, 15))
pos = nx.spring_layout(G, k=0.15, seed=3040)
node_color = ["blue" if G.degree[node] != 0 else "white" for node in G.nodes()]
node_size = [G.degree[node] for node in G.nodes()]
# edge_color = [rgb_creator(community_index_Aut[n[0]], max_index) if community_index_Aut[n[0]] == community_index_Aut[n[1]] else (0.9, 0.9, 0.9) for n in nx.edges(H)]
nx.draw_networkx(G, pos=pos, with_labels=False, node_color=node_color, node_size=node_size, edge_color="black", alpha=0.7)
fig.tight_layout()
plt.axis("off")
plt.show()
"""

