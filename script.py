from CharacterNames import create_character_graph
from DrawGraph import draw_plotly, draw_plotly_weighted

adr = "./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt"

print("creating graph")
G, names, counts = create_character_graph(adr)
print("name\t count")
for i in range(len(names)):
    print(f'{names[i]}\t{counts[i]}')

draw_plotly(G, names)