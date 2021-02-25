import networkx as nx
import plotly.graph_objects as go


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
        node_text.append('# of connections: ' + str(len(adjacencies[1])) +
                         '\n/ count: ' + str(G.nodes(data=True)[node]['count']) +
                         '\n/ degree: ' + str(G.degree(node)))
    node_trace.marker.color = node_adjacencies
    node_trace.hovertext = node_text
    node_trace.text = list(G)
    return node_trace


def _make_edge(x, y, text, width):
    """
    create two traces one for the edge with the specified width,
    other for the label in the middle of the edge
    :param x , y: array of xs and ys of start and end of the edge
    :param text: edge label
    :param width: edge width
    :return: two traces
    """
    x_mid = [(x[0]+x[1])/2]
    y_mid = [(y[0]+y[1])/2]
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


def _make_edge_traces(G):
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
                trace1, trace2 = _make_edge([x0, x1, None], [y0, y1, None], w,
                                            0.3 * w)
                edge_trace.append(trace1)
                edge_trace.append(trace2)
    return edge_trace


def draw_plotly_MultiGraph(G):
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

    edge_traces = _make_edge_traces(G)
    node_trace = _make_node_trace(G)

    layout = go.Layout(
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
    node_ids = list(G)
    for i in range(len(node_ids)):
        for j in range(i + 1, len(node_ids)):
            u = node_ids[i]
            v = node_ids[j]
            if G.get_edge_data(u, v) is not None:
                x0, y0 = G.nodes[u]['pos']
                x1, y1 = G.nodes[v]['pos']
                w = len(G.get_edge_data(u, v))
                trace1, trace2 = _make_edge([x0, x1, None], [y0, y1, None], w,
                                            0.3 * w)
                edge_trace.append(trace1)
                edge_trace.append(trace2)

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
