import pandas as pd
import os
import GraphProssesing
import networkx as nx
import plotly.express as px

df = pd.read_csv("./Metadata_complete_info.csv",
                 converters={'subjects_list': eval, 'subjects_list_separated': eval})
df['graph_size_ratio'] = -1
df.loc[(df.graph_size > -1) & (df.central_graph_size > 0), 'graph_size_ratio'] = \
df[(df.graph_size > -1) & (df.central_graph_size > 0)]['central_graph_size'].values / \
df[(df.graph_size > -1) & (df.central_graph_size > 0)]['graph_size'].values


def get_rows_with_list_key_values(df, list_key, values):
    return df[pd.DataFrame(df[list_key].tolist()).isin(values).any(1).values].copy()


def get_book_subjects(df, book_name):
    return df.loc[df['name'] == book_name]['subjects_list'].values[0]


def get_all_subjects(df, key):
    all_subjects = {}
    for i in df[key]:
        for j in i:
            if j in all_subjects.keys():
                all_subjects[j] += 1
            else:
                all_subjects[j] = 1
    return [(i, all_subjects[i]) for i in sorted(all_subjects, key=lambda x: all_subjects[x], reverse=True)]


def read_df():
    if os.path.exists("./Metadata_with_graph_info.csv"):
        df = pd.read_csv("./Metadata_with_graph_info.csv",
                         converters={'subjects_list': eval, 'subjects_list_separated': eval})
    else:
        print("didn't find Metadata_with_graph_info. Creating ...")
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

        df['subjects_list_separated'] = None
        for i in df.index:
            subjects = df.iloc[i]['subjects_list'].copy()
            l = set()
            for s in subjects:
                l = l.union([j.strip() for j in s.split("--")])
            df.at[i, 'subjects_list_separated'] = list(l)
        import CategoryGraph
        cms = CategoryGraph.community_index
        for i in cms:
            df.loc[df.name == i, 'category_community'] = cms[i]
        df.to_csv("./Metadata_with_graph_info.csv")
    return df


def get_repeated_subjects_as_tags(df, key, min_number):
    sdf = pd.DataFrame()
    for tag, rep in get_all_subjects(df, key):
        if rep >= min_number:
            n = get_rows_with_list_key_values(df, key, [tag])
            n['tag'] = tag
            sdf = sdf.append(n)
    return sdf


def get_subjects_as_tags(df, key, values):
    sdf = pd.DataFrame()
    for tag in values:
        n = get_rows_with_list_key_values(df, key, [tag])
        n['tag'] = tag
        sdf = sdf.append(n)
    return sdf


def graph_size_box_plot(sdf):
    fig = px.box(sdf, x="tag", y="graph_size",
                 notched=True,  # used notched shape
                 title="Box plot",
                 hover_data=["tag"]  # add day column to hover data
                 )
    fig.show()


def graph_size_mean_bar_plot(sdf):
    a = sdf.groupby('tag').graph_size.mean().reset_index()
    a.sort_values(by='graph_size', ascending=False)
    fig = px.bar(a, x='tag', y='graph_size')
    fig.show()


def find_category_labels(df):
    category_labels = {}
    for cat, data in df.groupby('category_community'):
        category_labels[cat] = {'separated': [], 'combined': []}
        print(type(data))
        for j in data.subjects_list_separated.values:
            category_labels[cat]['separated'].extend(j)
        for j in data.subjects_list.values:
            category_labels[cat]['combined'].extend(j)
    return category_labels


def select_repeated(df, key, count):
    vc = df.value_counts(key) > count
    vc = vc[vc]
    return df.loc[df[key].isin(vc.index)].copy()


def subject_frequency_per_subjects(df, key):
    s = get_all_subjects(df, key)
    sums = sum([a[1] for a in s])
    return [(a[0], a[1] / sums) for a in s]


def subject_frequency_per_books(df, key):
    s = get_all_subjects(df, key)
    return [(a[0], a[1] / len(df)) for a in s]


def subject_frequency_diff(df1, df2, key, per_subjects=False):
    if per_subjects:
        f1 = subject_frequency_per_subjects(df1, key)
        f2 = subject_frequency_per_subjects(df2, key)
    else:
        f1 = subject_frequency_per_books(df1, key)
        f2 = subject_frequency_per_books(df2, key)
    d1 = dict(f1)
    d2 = dict(f2)
    result = {}
    for d in d1:
        if d not in result:
            result[d] = d1[d]
    for d in d2:
        if d in result:
            result[d] = abs(result[d] - d2[d])
        else:
            result[d] = d2[d]
    result = [(a, result[a]) for a in result]
    return sorted(result, key=lambda x: x[1], reverse=True)
