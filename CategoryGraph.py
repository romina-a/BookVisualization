import csv
import networkx as nx


list = []
G = nx.Graph()
with open('./Metadata.csv', 'r', encoding='cp1252') as file:
    reader = csv.reader(file)
    for row in reader:
        category_string = row[5]
        while '"' in category_string:
            category_string = category_string.replace('"', "'")
        while r"\\" in category_string:
            category_string = category_string.replace(r'\\', "")
        category_string = category_string.replace("['", "")
        category_string = category_string.replace("']", "")
        category_list = category_string.split("', '")

        list.append([row[0], category_list])
        G.add_node(row[0])

file.close()

for x in list:
    for y in list:
        if not (G.has_edge(x[0], y[0])) and x[0] != y[0]:
            if len(set(x[1]).intersection(set(y[1]))) > 0:
                G.add_edge(x[0], y[0])


# largest connected component
components = nx.connected_components(G)
largest_component = max(components, key=len)
H = G.subgraph(largest_component)

# compute community structure
lpc = nx.community.label_propagation_communities(H)
community_index = {n: i for i, com in enumerate(lpc) for n in com}

# community index, categories, name
for community in community_index:
    index_row = [list.index(row) for row in list if community in row]
    print(community_index[community], list[index_row[0]][1], community)

# nx.write_gpickle(G, './CategoriesGraph.gpickle')
