import networkx as nx

"""
A Character Graph must have the following attributes:
            -graph attributes (G.graph()):
                             'end_time': int, the last time_stamp
            -node attributes (G.nodes(data=True)[<node_id>]):
                             'count': int, total #times the character name was found in the book
                             'pos': tuple, (x,y) set based on the layout for drawing
            -edge attributes (G.edges(data=True)[<u_id>,<v_id>, key]]/G.get_edge_data(<u_id>,<v_id>)):
                             'time': time stamps representing when u and v appeared closer than max_dist

Graph G represents a simple Character Graph
"""

# adding nodes with count attribute
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

# adding edges with time attribute
G.add_edge("Romina", "Abadi", time=1)
G.add_edge("Romina", "Abadi", time=2)
G.add_edge("Romina", "Abadi", time=3)
G.add_edge("Romina", "Amin", time=1)
G.add_edge("Romina", "Amin", time=3)
G.add_edge("Mrs. Abadi", "Soghra", time=2)
G.add_edge("Soghra", "Mrs. Romina Abadi", time=4)
G.add_edge("Amin", 'Abadi', time=4)
G.add_edge("Amin", "Gholi Abadi", time=2)

# adding end_time attribute to the graph
G.graph['end_time'] = 4


pos = nx.spring_layout(G)
nx.set_node_attributes(G, pos, 'pos')


# DrawGraph.draw_graph_plotly(G, graph_type='multi')

