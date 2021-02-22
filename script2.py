from CharacterNames import create_character_MultiGraph, merge_similar_nodes
from DrawGraph import draw_plotly, draw_plotly_weighted
import time
import networkx as nx

book_name = "Charles Dickens___A Christmas Carol"
cc_adr = "./Data/Gutenberg/txt/"+book_name+".txt"

# creating the graph and timing the process
print("creating the graph...")
t = time.time()
G = create_character_MultiGraph(cc_adr, max_dist=30)
print("%%%% took:{}s".format(time.time()-t))

# printing the names
print("before merging")
print("name\t count")
for i in list(G):
    print(f'{i}\t{G.nodes[i]["count"]}')
draw_plotly(G, 'multi graph before merging')

# save the graph, can load with G = nx.read_gpickle("./<name>.gpickle")
nx.write_gpickle(G, f'./{book_name}_seprate.gpickle')

# merging
merge_similar_nodes(G)

# printing nodes after merge
print("after merging")
print("name\t count")
for i in list(G):
    print(f'{i}\t{G.nodes[i]["count"]}')

# printing the merged ones
print("merged:")
for i in list(G):
    if "contraction" in G.nodes[i]:
        print(f'{i}\t{list(G.nodes[i]["contraction"].keys())}')

draw_plotly(G, 'multi graph after merging')

# save the graph, can load with G = nx.read_gpickle("./<name>.gpickle")
nx.write_gpickle(G, f'./{book_name}_merged.gpickle')
