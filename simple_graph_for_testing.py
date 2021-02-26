import networkx as nx
import CharacterNames
import DrawGraph


G = nx.MultiGraph()
G.add_node("Romina", count=3)
G.add_node("Abadi", count=2)
G.add_node("Mrs. Romina Abadi", count=1)
G.add_node("Mrs. Abadi", count=3)
G.add_node("Gholi Abadi", count=1)
G.add_node("Gholi J. Abadi")
G.add_node("Amin", count=4)
G.add_node("Amin Ghasemzadeh", count=1)
G.add_node("Soghra", count=1)

G.add_edge("Romina", "Abadi", time=1)
G.add_edge("Romina", "Abadi", time=1)
G.add_edge("Romina", "Abadi", time=1)
G.add_edge("Romina", "Amin", time=1)
G.add_edge("Romina", "Amin", time=1)
G.add_edge("Mrs. Abadi", "Soghra", time=1)
G.add_edge("Soghra", "Mrs. Romina Abadi", time=1)
G.add_edge("Amin", 'Abadi', time=1)
G.add_edge("Amin", "Gholi Abadi", time=1)

DrawGraph.draw_graph_plotly(G, graph_type='multi', layout='spring')
print("G nodes:")
for c in G.nodes():
    print("{}:{}".format(c, G.nodes(data=True)[c]))
print("G edges:")
