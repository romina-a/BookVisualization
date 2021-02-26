from CharacterNames import create_character_MultiGraph, merge_similar_nodes
from DrawGraph import draw_graph_plotly as draw
import time
import networkx as nx
import GraphProssesing

# TODO create function to accept different books

book_name = "Charles Dickens___A Christmas Carol"
# book_name = "Charles Dickens___Oliver Twist"
cc_adr = "./Data/Gutenberg/txt/"+book_name+".txt"

# creating the graph and timing the process
print("creating the graph...")
t = time.time()
G = create_character_MultiGraph(cc_adr, max_dist=30)
print("%%%% took:{}s".format(time.time()-t))

# save the graph, can load with G = nx.read_gpickle("./<name>.gpickle")
nx.write_gpickle(G, f'./SavedGraphs/{book_name}_separate.gpickle')

# print the names
print("before merging")
print("name\t count")
for i in list(G):
    print(f'{i}\t{G.nodes[i]["count"]}')
draw(G, 'multi graph before merging')


# merge
merge_similar_nodes(G)

# print nodes after merge
print("after merging")
print("name\t count")
for i in list(G):
    print(f'{i}\t{G.nodes[i]["count"]}')

# print the merged ones
print("merged:")
for i in list(G):
    if "contraction" in G.nodes[i]:
        print(f'{i}\t{list(G.nodes[i]["contraction"].keys())}')

draw(G, 'multi graph after merging')

# largest connected component
largest_cc = max(nx.connected_components(G), key=len)
G_main = G.subgraph(largest_cc).copy()
draw(G_main, 'multi graph largest cc after merging')

# highest degree nodes:
highs = GraphProssesing.find_highest_deg(G, 20)
print("highest degree nodes are:\n\t{}".format(highs))
G_high = G.subgraph(highs).copy()
draw(G_high, 'after merging highest degree nodes')

GraphProssesing.plot_degree_dist(G)
