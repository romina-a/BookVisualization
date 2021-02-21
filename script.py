from CharacterNames import create_character_graph
from DrawGraph import draw_plotly, draw_plotly_weighted
import time

cc_adr = "./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt"
test_adr = "./Data/test.txt"

# creating the graph and timing the process
print("creating graph...")
t = time.time()
G, names, counts = create_character_graph(cc_adr, max_dist=30)
print("%%%% took:{}s".format(time.time()-t))

# printing the names
print("name\t count")
for i in range(len(names)):
    print(f'{names[i]}\t{counts[i]}')

draw_plotly(G, names)