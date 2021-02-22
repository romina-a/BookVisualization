import networkx as nx
import CharacterNames
import DrawGraph

G = nx.MultiGraph()
G.add_node("Romina", count=1)
G.add_node("Mrs. Romina", count=1)
G.add_node("Mrs. Romina Abadi", count=1)
G.add_node("Mrs. Abadi", count=1)
G.add_node("Amin", count=1)
G.add_node("Amin Ghasemzadeh", count=1)
G.add_node("Soghra", count=1)

G.add_edge("Romina", "Mrs. Romina", t=1)
G.add_edge("Romina", "Mrs. Romina", t=1)
G.add_edge("Romina", "Mrs. Romina", t=1)
G.add_edge("Romina", "Amin", t=1)
G.add_edge("Romina", "Amin", t=1)
G.add_edge("Mrs. Abadi", "Soghra", t=1)
G.add_edge("Soghra", "Romina", t=1)


def test_names_similar():
    for u in list(G):
        for v in list(G):
            print(f'{u}\t{v}\t{CharacterNames._names_similar(u, v)}')


def test_similarity_graph():
    DrawGraph.draw_plotly(G)
    Gsim = CharacterNames._similarity_graph(G)
    DrawGraph.draw_plotly(Gsim)
    return Gsim


def test_merge_nodes_1():
    Gcopy = G.copy()

    DrawGraph.draw_plotly(G, 'G')
    print("G nodes:")
    for c in G.nodes():
        print("{}:{}".format(c, Gcopy.nodes(data=True)[c]))
    print("G edges:")
    for e in G.edges(data=True):
        print(e)

    CharacterNames._merge_nodes(Gcopy, ['Mrs. Abadi', 'Mrs. Romina'])
    DrawGraph.draw_plotly(Gcopy, 'merged Mrs. Abadi, Mrs. Romina')

    CharacterNames._merge_nodes(Gcopy, ['Romina', 'Amin Ghasemzadeh'])
    DrawGraph.draw_plotly(Gcopy, 'merged Mrs. Abadi, Mrs. Romina/ '
                                 'Romina, Amin Ghasemzadeh')
    CharacterNames._merge_nodes(Gcopy, ['Mrs. Romina', 'Amin Ghasemzadeh'])
    DrawGraph.draw_plotly(Gcopy, 'merged Mrs. Abadi, Mrs. Romina/ '
                                 'Romina, Amin Ghasemzadeh/ '
                                 'Mrs. Romina, Amin Ghasemzadeh')
    print('merged Mrs. Abadi, Mrs. Romina/ '
          'Romina, Amin Ghasemzadeh/ '
          'Mrs. Romina, Amin Ghasemzadeh')
    print("Gcopy nodes:")
    for c in Gcopy.nodes():
        print("{}:{}".format(c, Gcopy.nodes(data=True)[c]))
    print("Gcopy edges:")
    for e in Gcopy.edges(data=True):
        print(e)
    return Gcopy


def test_merge_nodes_2():
    Gcopy = G.copy()
    DrawGraph.draw_plotly(G, 'G')
    print("G nodes:")
    for c in G.nodes():
        print("{}:{}".format(c, Gcopy.nodes(data=True)[c]))
    print("G edges:")
    for e in G.edges(data=True):
        print(e)
    CharacterNames._merge_nodes(Gcopy, ['Mrs. Abadi', 'Mrs. Romina', 'Amin Ghasemzadeh'])
    DrawGraph.draw_plotly(Gcopy, 'merged Mrs. Abadi, Mrs. Romina, Amin Ghasemzadeh')
    print("Gcopy nodes:")
    for c in Gcopy.nodes():
        print("{}:{}".format(c, Gcopy.nodes(data=True)[c]))
    print("Gcopy edges:")
    for e in Gcopy.edges(data=True):
        print(e)
    return Gcopy


def test_merge_similar_nodes():
    DrawGraph.draw_plotly(G, 'G')
    print("G nodes:")
    for c in G.nodes():
        print("{}:{}".format(c, Gcopy.nodes(data=True)[c]))
    print("G edges:")

    Gcopy=G.copy
    CharacterNames.merge_similar_nodes(Gcopy)

    DrawGraph.draw_plotly(Gcopy, 'Gcopy')
    print("Gcopy nodes:")
    for c in Gcopy.nodes():
        print("{}:{}".format(c, Gcopy.nodes(data=True)[c]))
    print("Gcopy edges:")
    for e in Gcopy.edges(data=True):
        print(e)
    return Gcopy