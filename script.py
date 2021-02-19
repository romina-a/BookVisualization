from CharacterNames import create_character_graph
from DrawGraph import draw

book_address = "C:/Users/amin/OneDrive - York University/Courses/Data analysis and " \
               "visualization/Projects/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt "

print("creating graph")
G, names, counts = create_character_graph(book_address)
print("name\t count")
for i in range(len(names)):
    print(f'{names[i]}\t{counts[i]}')
draw(G, names)
