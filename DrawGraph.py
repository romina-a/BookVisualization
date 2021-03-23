import networkx as nx
import plotly.graph_objects as go


# TODO add more hover points for edges, improve hover text (show u and v)
# TODO degree is not right for weighted graph (we might not need a weighted graph version!)
def _make_node_trace(G, node_colors=None):
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

    node_text = []
    for i, adjacencies in enumerate(G.adjacency()):
        node = list(G)[i]
        count_str = "--" if 'count' not in G.nodes(data=True)[node] else str(G.nodes(data=True)[node]['count'])
        color_scale = "--" if node_colors is None else str(node_colors[i])
        node_text.append(node+':'
                         '# of connections: ' + str(len(adjacencies[1])) +
                         '\n/ count: ' + count_str +
                         '\n/ degree: ' + str(G.degree(node)) +
                         '\n/ rank: ' + color_scale)
    # Scale the edge color based on node_colors if not provided, degree is used
    node_trace.marker.color = node_colors if node_colors is not None else [i[1] for i in G.degree()]
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


def draw_graph_plotly(G, graph_title="", graph_type="multi", save_adr=None, node_colors=None):
    """
        WARNING: You must set the layout first
        WARNING: Degree is not right for weighted graphs
        Source: https://github.com/rweng18/midsummer_network/blob/master/midsummer_graph.ipynb

        :param G: nx.Graph
        :param graph_title: string, the title is shown on top left of the graphs
        :param graph_type: type of G_Sim, options: "multi", "weighted", "simple"
        :param save_adr: string, full address to save the figure (e.g. "./figures/figure.png")
        :param node_colors: list of int, determine the scale for node colors if not provided: degree
    """

    if graph_type.lower() == "multi":
        edge_traces = _make_edge_traces_multi(G)
    elif graph_type.lower() == "weighted":
        edge_traces = _make_edge_traces_weighted(G)
    else:
        edge_traces = _make_edge_traces_simple(G)

    node_trace = _make_node_trace(G, node_colors=node_colors)

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
    if save_adr is not None:
        fig.write_image(save_adr)
    fig.show()
