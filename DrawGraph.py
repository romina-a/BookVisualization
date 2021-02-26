import networkx as nx
import plotly.graph_objects as go
from math import exp
import matplotlib.pyplot as plt
# TODO make it one


# TODO add more hover points for edges
def _make_node_trace(G):
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=5,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=0.1))

    node_adjacencies = []
    node_text = []
    for i, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node = list(G)[i]
        count_str = "--" if 'count' not in G.nodes(data=True)[node] else str(G.nodes(data=True)[node]['count'])
        node_text.append('# of connections: ' + str(len(adjacencies[1])) +
                         '\n/ count: ' + count_str +
                         '\n/ degree: ' + str(G.degree(node)))
    node_trace.marker.color = node_adjacencies
    node_trace.hovertext = node_text
    node_trace.text = list(G)
    return node_trace


def _make_edge_trace(x, y, text, width):
    """
    create two traces one for the edge with the specified width,
    other for the label in the middle of the edge
    :param x , y: array of xs and ys of start and end of the edge
    :param text: edge label
    :param width: edge width
    :return: two traces
    """
    x_mid = [(x[0] + x[1]) / 2]
    y_mid = [(y[0] + y[1]) / 2]
    texts = [text]
    return go.Scatter(x=x,
                      y=y,
                      line=dict(width=width,
                                color='cornflowerblue', ),
                      mode='lines'), \
           go.Scatter(x=x_mid,
                      y=y_mid,
                      text=texts,
                      hoverinfo='text',
                      marker=dict(color='rgb(125,125,125)', size=1),
                      mode='markers'
                      )


def _make_edge_traces_multi(G):
    edge_trace = []
    node_ids = list(G)
    for i in range(len(node_ids)):
        for j in range(i + 1, len(node_ids)):
            u = node_ids[i]
            v = node_ids[j]
            if G.get_edge_data(u, v) is not None:
                x0, y0 = G.nodes[u]['pos']
                x1, y1 = G.nodes[v]['pos']
                w = len(G.get_edge_data(u, v))
                trace1, trace2 = _make_edge_trace([x0, x1, None], [y0, y1, None], w,
                                                  min(max(0.1, 0.5 * w), 5))
                edge_trace.append(trace1)
                edge_trace.append(trace2)
    return edge_trace


def _make_edge_traces_weighted(G):
    edge_trace = []
    for e in G.edges(data=True):
        u = e[0]
        v = e[1]
        w = e[2]['weight']
        x0, y0 = G.nodes[u]['pos']
        x1, y1 = G.nodes[v]['pos']
        trace1, trace2 = _make_edge_trace([x0, x1, None], [y0, y1, None], w,
                                          min(max(1, 0.03 * w), 5))
        edge_trace.append(trace1)
        edge_trace.append(trace2)
    return edge_trace


def _make_edge_traces_simple(G):
    edge_trace = []
    for e in G.edges(data=True):
        u = e[0]
        v = e[1]
        x0, y0 = G.nodes[u]['pos']
        x1, y1 = G.nodes[v]['pos']
        trace1, trace2 = _make_edge_trace([x0, x1, None], [y0, y1, None], 1, 2)
        edge_trace.append(trace1)
        edge_trace.append(trace2)
    return edge_trace


layouts = {
    'spring': nx.spring_layout,
    'circular': nx.circular_layout,
    'kamada_kawai': nx.kamada_kawai_layout,
    'shell': nx.shell_layout,
}


def draw_graph_plotly(G, graph_title="", type="multi", layout="spring"):
    """
        Source: https://github.com/rweng18/midsummer_network/blob/master/midsummer_graph.ipynb

        :param G: networkx graph
        :param graph_title: the title is shown on top left of the graphs
        :param type: type of G, options: "multi", "weighted", "simple"
        :param layout: options: the layout for nodes, "spring", "circular", "kamada_kawai", "shell"
    """
    pos = layouts[layout](G)
    nx.set_node_attributes(G, pos, 'pos')

    if type.lower() == "multi":
        edge_traces = _make_edge_traces_multi(G)
    elif type.lower() == "weighted":
        edge_traces = _make_edge_traces_weighted(G)
    else:
        edge_traces = _make_edge_traces_simple(G)

    node_trace = _make_node_trace(G)

    layout = go.Layout(
        title='<br>' + graph_title,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig = go.Figure(layout=layout)
    for trace in edge_traces:
        fig.add_trace(trace)

    fig.add_trace(node_trace)

    fig.update_layout(showlegend=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    fig.show()


# Deprecated
# NOTE source: https://plotly.com/python/network-graphs/
def draw_plotly(G, graph_title="graph"):
    """
    If it doesn't work in PyCharm, run it in terminal.
    :param graph_title: the title to show on the plot
    :param G: networkx graph
    """

    pos = nx.spring_layout(G)
    # other layouts:
    # pos = nx.circular_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    # pos = nx.shell_layout(G)
    nx.set_node_attributes(G, pos, 'pos')
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=list(G),
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=20,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    # node_trace.text = node_text
    node_trace.text = list(G)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>' + graph_title,
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        # annotations=[dict(
                        #     text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        #     showarrow=False,
                        #     xref="paper", yref="paper",
                        #     x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()


def make_edge(x, y, text, width):
    '''Creates a scatter trace for the edge between x's and y's with given width
    Parameters
    ----------
    x    : a tuple of the endpoints' x-coordinates in the form, tuple([x0, x1, None])
    y    : a tuple of the endpoints' y-coordinates in the form, tuple([y0, y1, None])
    width: the width of the line
    Returns
    -------
    An edge trace that goes between x0 and x1 with specified width.
    '''
    return go.Scatter(x=x,
                      y=y,
                      line=dict(width=width,
                                color='cornflowerblue'),
                      hoverinfo='text',
                      text=([text]),
                      mode='lines')


def draw_plotly_weighted(G):
    """
    Source: https://github.com/rweng18/midsummer_network/blob/master/midsummer_graph.ipynb
    :param G: networkx graph
    :param labels: list of node names (to show when the mouse hovers over the node)
    """
    # pos = nx.spring_layout(G)
    # other layouts:
    # pos = nx.circular_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.shell_layout(G)
    nx.set_node_attributes(G, pos, 'pos')

    edge_trace = []
    for edge in G.edges(data=True):
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        w = edge[2]['weight']
        trace = make_edge([x0, x1, None], [y0, y1, None], w,
                          0.3 * w)
        edge_trace.append(trace)

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    # node_trace.text = node_text
    node_trace.text = list(G)

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig = go.Figure(layout=layout)

    for trace in edge_trace:
        fig.add_trace(trace)

    fig.add_trace(node_trace)

    fig.update_layout(showlegend=False)

    fig.update_xaxes(showticklabels=False)

    fig.update_yaxes(showticklabels=False)

    fig.show()
