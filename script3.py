from CharacterNames import create_character_graph
from DrawGraph import draw_plotly, draw_plotly_weighted
import time
import networkx as nx

# NOTE: DrawGraph.draw_plotly method has changed and does not accept separate
#  node label list. This scripts changes the output of the create_character_graph
#  to match the input of the new DrawGraph.draw_plotly

cc_adr = "./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt"
test_adr = "./Data/test.txt"

# creating the graph and timing the process
print("creating the graph...")
t = time.time()
G, names, counts = create_character_graph(cc_adr, max_dist=30)
print("%%%% took:{}s".format(time.time()-t))

d = {}
for i, n in enumerate(names):
    d[i] = n
nx.relabel.relabel_nodes(G, d, copy=False)

# printing the names
print("name\t count")
for i in range(len(names)):
    print(f'{names[i]}\t{counts[i]}')

draw_plotly(G, 'the simple one')


