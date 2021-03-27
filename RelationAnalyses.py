import pandas as pd
import os
import GraphProssesing
import networkx as nx


def get_rows_with_subjects(subjects):
    return df[pd.DataFrame(df.subjects_list.tolist()).isin(subjects).any(1).values]


def get_categories(book_name):
    return df.loc[df['name'] == book_name]['subjects_list'].values[0]


def get_all_subjects():
    all_subjects = {}
    for i in df.subjects_list.values:
        for j in i:
            if j in all_subjects.keys():
                all_subjects[j] += 1
            else:
                all_subjects[j] = 1


if os.path.exists("./Metadata_with_graph_info.csv"):
    df = pd.read_csv("./Metadata_with_graph_info.csv", converters={'subjects_list': eval})
else:
    df = pd.read_csv("./Metadata.csv", converters={'subjects_list': eval})

    df['graph_size'] = -1
    df['central_graph_size'] = -1
    df['fluidity_total'] = -1
    df['fluidity_central'] = -1

    for i, adr in enumerate(os.listdir("./SavedGraph")):
        g = nx.read_gpickle(os.path.join("./SavedGraph", adr))
        fname, ext = os.path.splitext(adr)
        author, name = fname.split("___")
        graph_size = len(g.nodes())
        central_graph_size = len(GraphProssesing.find_central_characters(g, 0.5))
        fluidity_total = sum(GraphProssesing.fluidity_total(g, 40))
        fluidity_central = sum(GraphProssesing.fluidity_central(g, 40))
        # print(f'name:{name}, author:{author}, size:{graph_size}')
        # print(df.loc[(df.name == name) & (df.author == author)])
        df.loc[(df.name == name) & (df.author == author), 'graph_size'] = graph_size
        df.loc[(df.name == name) & (df.author == author), 'central_graph_size'] = central_graph_size
        df.loc[(df.name == name) & (df.author == author), 'fluidity_total'] = fluidity_total
        df.loc[(df.name == name) & (df.author == author), 'fluidity_central'] = fluidity_central
        print(f"done {i}")
    df.to_csv("./Metadata_with_graph_info.csv")
