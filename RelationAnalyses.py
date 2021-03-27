import pandas as pd
import os
import GraphProssesing
import networkx as nx

df = pd.read_csv("./Metadata.csv", converters={'subjects_list': eval})

def extract_author_title_from_adr(adr):
    fname, ext = os.path.splitext(adr)
    author, name = fname.split("___")
    return author, name


def get_rows_with_subjects(subjects):
    return df[pd.DataFrame(df.subjects_list.tolist()).isin(subjects).any(1).values]


def get_categories(book_name):
    return df.loc[df['name'] == book_name]['subjects_list'].values[0]


all_subjects = {}
for i in df.subjects_list.values:
    for j in i:
        if j in all_subjects.keys():
            all_subjects[j] += 1
        else:
            all_subjects[j] = 1


df['graph_size'] = -1
df['graph_central_size'] = -1

for adr in os.listdir("./SavedGraphs"):
    g = nx.read_gpickle(os.path.join("./SavedGraphs", adr))
    fname, ext = os.path.splitext(adr)
    author, name = fname.split("___")
    graph_size = len(g.nodes())
    central_graph_size = len(GraphProssesing.central_characters(g, 0.5))
    print(f'name:{name}, author:{author}, size:{graph_size}')
    print(df.loc[(df.name == name) & (df.author == author)])
    df.loc[(df.name == name) & (df.author == author), 'graph_size'] = graph_size
    df.loc[(df.name == name) & (df.author == author), 'central_graph_size'] = central_graph_size


