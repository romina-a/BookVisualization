import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import RelationAnalyses

df = RelationAnalyses.df

# ~~~~~~~~~~~~~~~~~~~~~~ Authors ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

df_repeated_authors = RelationAnalyses.select_repeated(df, 'author', 50)
df_repeated_authors = df_repeated_authors[
    (df_repeated_authors.graph_size > -1) & (df_repeated_authors.central_graph_size) > 0]
df_repeated_authors_for_means = df_repeated_authors.groupby('author').mean().reset_index().sort_values(by='graph_size',
                                                                                                       ascending=False)
# ~~~~~~~~~ box plots together ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig = go.Figure()
fig.add_trace(go.Box(
    y=df_repeated_authors.graph_size.values,
    x=df_repeated_authors.author.values,
    name='graph_size',
    marker_color='#3D9970'
))
fig.add_trace(go.Box(
    y=df_repeated_authors.central_graph_size.values,
    x=df_repeated_authors.author.values,
    name='central_graph_size',
    marker_color='#FF4136'
))
fig.add_trace(go.Box(
    y=df_repeated_authors.graph_size_ratio.values,
    x=df_repeated_authors.author.values,
    name='ratio',
    marker_color='#FF851B'
))
fig.update_layout(
    yaxis_title='size',
    boxmode='group'  # group together boxes of the different traces for each value of x
)
fig.show()

# ~~~~~~~~~~~~~~~~~~~ Fluidity ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~```

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.05)
fig.add_trace(go.Box(
    y=df_repeated_authors.fluidity_total.values,
    x=df_repeated_authors.author.values,
    name='fluidity total',
    marker_color='#3D9970',
    # boxpoints=False
), row=1, col=1)
fig.add_trace(go.Box(
    y=df_repeated_authors.fluidity_central.values,
    x=df_repeated_authors.author.values,
    name='fluidity central',
    marker_color='#FF4136',
    # boxpoints=False
), row=2, col=1)
fig.update_yaxes(title_text="fluidity total", row=1, col=1)
fig.update_yaxes(title_text="fluidity central", row=2, col=1)
fig.update_layout(height=750, width=750)
fig.show()

# ~~~~~~~~~~~~~ Normalized fluidity ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.05)
fig.add_trace(go.Box(
    y=df_repeated_authors.fluidity_total.values / df_repeated_authors.graph_size.values,
    x=df_repeated_authors.author.values,
    name='fluidity total',
    marker_color='#3D9970',
    # boxpoints=False
), row=1, col=1)
fig.add_trace(go.Box(
    y=df_repeated_authors.fluidity_central.values / df_repeated_authors.graph_size.values,
    x=df_repeated_authors.author.values,
    name='fluidity central',
    marker_color='#FF4136',
    # boxpoints=False
), row=2, col=1)
fig.update_yaxes(title_text="fluidity total", row=1, col=1)
fig.update_yaxes(title_text="fluidity central", row=2, col=1)
fig.update_layout(height=750, width=750)
fig.show()

# ~~~~~~~~~~~~~~~ means together ~~~~~~~~~~~~~~~~~~~~~~~`
fig = go.Figure(data=[
    go.Bar(name='fluidity total',
           x=df_repeated_authors_for_means['author'],
           y=df_repeated_authors_for_means['fluidity_total']),
    go.Bar(name='fluidity central',
           x=df_repeated_authors_for_means['author'],
           y=df_repeated_authors_for_means['fluidity_central']),
    go.Bar(name='graph size',
           x=df_repeated_authors_for_means['author'],
           y=df_repeated_authors_for_means['graph_size']),
    go.Bar(name='graph size',
           x=df_repeated_authors_for_means['author'],
           y=df_repeated_authors_for_means['central_graph_size']),
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.show()

# ~~~~~~~~~~~~~~~~~~ means togehter 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

fig = go.Figure(data=[
    go.Bar(name='fluidity total',
           x=df_repeated_authors_for_means['author'],
           y=df_repeated_authors_for_means['fluidity_total'] / df_repeated_authors_for_means['graph_size']),
    go.Bar(name='fluidity central',
           x=df_repeated_authors_for_means['author'],
           y=df_repeated_authors_for_means['fluidity_central'] / df_repeated_authors_for_means['graph_size']),
    # go.Bar(name='graph size',
    # x=df_repeated_authors_for_means['author'],
    # y=df_repeated_authors_for_means['graph_size']),
    # go.Bar(name='central graph size',
    #            x=df_repeated_authors_for_means['author'],
    #            y=df_repeated_authors_for_means['central_graph_size']),
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.show()


# ~~~~~~~~~~~~ authors means separated ~~~~~~~~~~~~~~~~~~~~~~~~~~
def graph_size_and_authors_mean():
    df_repeated_authors = RelationAnalyses.select_repeated(df, 'author', 50)
    df_repeated_authors = df_repeated_authors[
        (df_repeated_authors.graph_size > -1) & (df_repeated_authors.central_graph_size) > 0]
    df_repeated_authors_for_means = df_repeated_authors.groupby('author').mean().reset_index().sort_values(
        by='graph_size',
        ascending=False)
    fig = make_subplots(rows=3, cols=2, shared_xaxes=True,
                        vertical_spacing=0.05)
    fig.add_trace(go.Bar(name='fluidity total',
                         x=df_repeated_authors_for_means['author'],
                         y=df_repeated_authors_for_means['popularity'],
                         text=df_repeated_authors_for_means['popularity'],
                         textposition='auto',
                         texttemplate="%{y:.2f}",
                         ),
                  row=1, col=2)
    fig.add_hline(y=df_repeated_authors_for_means['popularity'].mean(),
                  line_color='Black', line_dash='dash', line_width=0.5,
                  row=1, col=2)
    fig.add_trace(go.Bar(name='fluidity total',
                         x=df_repeated_authors_for_means['author'],
                         y=df_repeated_authors_for_means['fluidity_total'],
                         text=df_repeated_authors_for_means['fluidity_total'],
                         textposition='auto',
                         texttemplate="%{y:.2f}",
                         ),
                  row=2, col=2)
    fig.add_hline(y=df_repeated_authors_for_means['fluidity_total'].mean(),
                  line_color='Black', line_dash='dash', line_width=0.5,
                  row=2, col=2)
    fig.add_trace(go.Bar(name='fluidity central',
                         x=df_repeated_authors_for_means['author'],
                         y=df_repeated_authors_for_means['fluidity_central'],
                         text=df_repeated_authors_for_means['fluidity_central'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=3, col=2)
    fig.add_hline(y=df_repeated_authors_for_means['fluidity_central'].mean(),
                  line_color='Black', line_dash='dash', line_width=0.5,
                  row=3, col=2)
    fig.add_trace(go.Bar(name='graph size',
                         x=df_repeated_authors_for_means['author'],
                         y=df_repeated_authors_for_means['graph_size'],
                         text=df_repeated_authors_for_means['graph_size'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=1, col=1)
    fig.add_hline(y=df_repeated_authors_for_means['graph_size'].mean(),
                  line_color='Black', line_dash='dash', line_width=0.5,
                  row=1, col=1)
    fig.add_trace(go.Bar(name='central graph size',
                         x=df_repeated_authors_for_means['author'],
                         y=df_repeated_authors_for_means['central_graph_size'],
                         text=df_repeated_authors_for_means['central_graph_size'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=2, col=1)
    fig.add_hline(y=df_repeated_authors_for_means['central_graph_size'].mean(),
                  line_color='Black', line_dash='dash', line_width=0.5,
                  row=2, col=1)
    fig.add_trace(go.Bar(name='ratio',
                         x=df_repeated_authors_for_means['author'],
                         y=df_repeated_authors_for_means['graph_size_ratio'],
                         text=df_repeated_authors_for_means['graph_size_ratio'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=3, col=1)
    fig.add_hline(y=df_repeated_authors_for_means['graph_size_ratio'].mean(),
                  line_color='Black', line_dash='dash', line_width=0.5,
                  row=3, col=1)
    fig.update_yaxes(title_text="graph size", showticklabels=False, row=1, col=1)
    fig.update_yaxes(title_text="central graph size", showticklabels=False, row=2, col=1)
    fig.update_yaxes(title_text="ratio", showticklabels=False, row=3, col=1)
    fig.update_yaxes(title_text="popularity", showticklabels=False, row=2, col=1)
    fig.update_yaxes(title_text="fluidity total", showticklabels=False, row=2, col=2)
    fig.update_yaxes(title_text="fluidity central", showticklabels=False, row=3, col=2)

    fig.update_layout(
        font=dict(
            size=8
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(zeroline=True, zerolinecolor='LightGrey', zerolinewidth=.1, showline=True, linecolor='Grey',
                     showgrid=True, gridwidth=.1, gridcolor='LightGrey')
    fig.update_xaxes(showline=True, linecolor='Grey')

    fig.write_image("./images/graph_size_and_authors_mean.pdf")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ box plots authors ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def graph_size_authors_box():
    df_repeated_authors = RelationAnalyses.select_repeated(df, 'author', 0)
    df_repeated_authors = df_repeated_authors[
        (df_repeated_authors.graph_size > -1) & (df_repeated_authors.central_graph_size) > 0]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.05)
    fig.add_trace(go.Box(
        y=df_repeated_authors.graph_size.values,
        x=df_repeated_authors.author.values,
        name='graph size',
        marker_color='#3D9970',
        # boxpoints=False
    ), row=1, col=1)
    fig.add_trace(go.Box(
        y=df_repeated_authors.central_graph_size.values,
        x=df_repeated_authors.author.values,
        name='central graph size',
        marker_color='#FF4136',
        # boxpoints=False
    ), row=2, col=1)
    fig.add_trace(go.Box(
        y=df_repeated_authors.graph_size_ratio.values,
        x=df_repeated_authors.author.values,
        name='ratio',
        marker_color='#FF851B',
        # boxpoints=False
    ), row=3, col=1)
    fig.update_yaxes(title_text="number of characters", row=1, col=1)
    fig.update_yaxes(title_text="number of central characters", row=2, col=1)
    fig.update_yaxes(title_text="ratio", row=3, col=1)
    # fig.update_layout(height=1500, width=750)

    fig.update_layout(
        font=dict(
            size=8
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(zeroline=True, zerolinecolor='LightGrey', zerolinewidth=.1, showline=True, linecolor='Grey',
                     showgrid=True, gridwidth=.1, gridcolor='LightGrey')
    fig.update_xaxes(showline=True, linecolor='Grey')
    fig.write_image("./images/graph_size_and_authors_box.pdf")

    fig.show()


# ~~~~~~~~~~~~~~~~~~~ category community ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def graph_size_category_community():
    # not used yet
    df_cats = RelationAnalyses.select_repeated(df, 'category_community', 100)
    df_cats = df_cats[
        (df_cats.graph_size > -1) & (df_cats.central_graph_size > 0) & (df_cats.category_community > -1)]
    df_cats_for_means = df_cats.groupby('category_community').mean().reset_index().sort_values(by='graph_size',
                                                                                               ascending=False)
    fig = make_subplots(rows=3, cols=2, shared_xaxes=True,
                        vertical_spacing=0.05)
    fig.add_trace(go.Bar(name='fluidity total',
                         x=[str(a) for a in df_cats_for_means['category_community']],
                         y=df_cats_for_means['fluidity_total'],
                         text=df_cats_for_means['fluidity_total'],
                         textposition='auto',
                         texttemplate="%{y:.2f}",
                         ),
                  row=2, col=2)
    fig.add_trace(go.Bar(name='fluidity central',
                         x=[str(a) for a in df_cats_for_means['category_community']],
                         y=df_cats_for_means['fluidity_central'],
                         text=df_cats_for_means['fluidity_central'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=3, col=2)
    fig.add_trace(go.Bar(name='graph size',
                         x=[str(a) for a in df_cats_for_means['category_community']],
                         y=df_cats_for_means['graph_size'],
                         text=df_cats_for_means['graph_size'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=1, col=1)
    fig.add_trace(go.Bar(name='central graph size',
                         x=[str(a) for a in df_cats_for_means['category_community']],
                         y=df_cats_for_means['central_graph_size'],
                         text=df_cats_for_means['central_graph_size'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=2, col=1)
    fig.add_trace(go.Bar(name='ratio',
                         x=[str(a) for a in df_cats_for_means['category_community']],
                         y=df_cats_for_means['graph_size_ratio'],
                         text=df_cats_for_means['graph_size_ratio'],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ),
                  row=3, col=1)
    fig.update_yaxes(title_text="graph size", showticklabels=False, row=1, col=1)
    fig.update_yaxes(title_text="central graph size", showticklabels=False, row=2, col=1)
    fig.update_yaxes(title_text="ratio", showticklabels=False, row=3, col=1)
    fig.update_yaxes(title_text="fluidity total", showticklabels=False, row=2, col=2)
    fig.update_yaxes(title_text="fluidity central", showticklabels=False, row=3, col=2)


# ~~~~~~~~~~~~ tags ~~~~~~~~~~~~~~~~~~~~~~~~~~
def graph_size_and_tags():
    # tags = RelationAnalyses.get_all_subjects(df, 'subjects_list_separated')
    # df_tags = RelationAnalyses.get_subjects_as_tags(df, 'subjects_list_separated', [a[0] for a in tags if a[1] > 20])
    df_tags = RelationAnalyses.get_subjects_as_tags(df, 'subjects_list_separated', ['Biography',
                                                                                    'History',
                                                                                    'Juvenile fiction',
                                                                                    'Science fiction',
                                                                                    'Fantasy fiction'
                                                                                    'Juvenile literature',
                                                                                    'Love stories',
                                                                                    'Drama',
                                                                                    'Detective and mystery stories',
                                                                                    'Short stories',
                                                                                    'Poetry',
                                                                                    'History',
                                                                                    'Bildungsromans'
                                                                                    'Historical fiction',
                                                                                    'Fiction'])
    # df_tags = RelationAnalyses.get_subjects_as_tags(RelationAnalyses.get_rows_with_list_key_values(df,'subjects_list_separated',['Fiction']),'subjects_list_separated',[a[0] for a in tags if a[1]>30])
    df_tags = df_tags[
        (df_tags.graph_size > -1) & (df_tags.central_graph_size) > 0]
    df_tags_for_means = df_tags.groupby('tag').mean().reset_index().sort_values(by='graph_size', ascending=False)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.05)
    # fig.add_trace(go.Bar(name='fluidity total',
    #                      x=df_tags_for_means['tag'],
    #                      y=df_tags_for_means['fluidity_total'],
    #                      text=df_tags_for_means['fluidity_total'],
    #                      textposition='auto',
    #                      texttemplate="%{y:.2f}",
    #                      ),
    #               row=2, col=2)
    # fig.add_trace(go.Bar(name='fluidity central',
    #                      x=df_tags_for_means['tag'],
    #                      y=df_tags_for_means['fluidity_central'],
    #                      text=df_tags_for_means['fluidity_central'],
    #                      textposition='auto',
    #                      texttemplate="%{y:.2f}"
    #                      ),
    #               row=3, col=2)
    fig.add_trace(go.Bar(name='graph size',
                         x=df_tags_for_means['tag'],
                         y=df_tags_for_means['graph_size'],
                         text=df_tags_for_means['graph_size'],
                         width=[.5 for _ in range(len(df_tags_for_means['graph_size']))]
                         # textposition='auto',
                         # texttemplate="%{y:.2f}"
                         ),
                  row=1, col=1)
    fig.add_hline(y=df_tags_for_means['graph_size'].mean(), line_color='Black', line_dash='dash', line_width=0.5, row=1,
                  col=1)
    fig.add_trace(go.Bar(name='central graph size',
                         x=df_tags_for_means['tag'],
                         y=df_tags_for_means['central_graph_size'],
                         text=df_tags_for_means['central_graph_size'],
                         width=[.5 for _ in range(len(df_tags_for_means['central_graph_size']))]
                         # textposition='auto',
                         # texttemplate="%{y:.2f}"
                         ),
                  row=2, col=1)
    fig.add_hline(y=df_tags_for_means['central_graph_size'].mean(), line_color='Black', line_dash='dash',
                  line_width=0.5, row=2, col=1)
    fig.add_trace(go.Bar(name='ratio',
                         x=df_tags_for_means['tag'],
                         y=df_tags_for_means['graph_size_ratio'],
                         text=df_tags_for_means['graph_size_ratio'],
                         width=[.5 for _ in range(len(df_tags_for_means['graph_size_ratio']))]
                         # textposition='auto',
                         # texttemplate="%{y:.2f}",
                         ),
                  row=3, col=1)
    fig.add_hline(y=df_tags_for_means['graph_size_ratio'].mean(), line_color='Black', line_dash='dash', line_width=0.5,
                  row=3, col=1)
    fig.update_yaxes(title_text="graph size", showticklabels=True, row=1, col=1)
    fig.update_yaxes(title_text="central graph size", showticklabels=True, row=2, col=1)
    fig.update_yaxes(title_text="ratio", showticklabels=True, row=3, col=1)
    fig.update_yaxes(title_text="fluidity total", showticklabels=False, row=2, col=2)
    fig.update_yaxes(title_text="fluidity central", showticklabels=False, row=3, col=2)

    fig.update_layout(
        font=dict(
            size=8
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(zeroline=True, zerolinecolor='LightGrey', zerolinewidth=.1, showline=True, linecolor='Grey',
                     showgrid=True, gridwidth=.1, gridcolor='LightGrey')
    fig.update_xaxes(showline=True, linecolor='Grey')
    # fig.write_image("./images/graph_size_and_tags_selected.pdf")
    fig.write_image("./images/graph_size_and_tags.pdf")


# ~~~~~~~~~~~~~~~~~~ similarity community ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
def graph_size_for_similarity_commmunity():
    df_cats = RelationAnalyses.select_repeated(df, 'similarity_community', 1000)
    df_cats = df_cats[
        (df_cats.graph_size > -1) & (df_cats.central_graph_size > 0) & (df_cats.similarity_community > -1)]
    df_cats_for_means = df_cats.groupby('similarity_community').mean().reset_index().sort_values(by='graph_size',
                                                                                                 ascending=False)
    fig = make_subplots(rows=1, cols=3, shared_xaxes=True,
                        vertical_spacing=0.05)
    fig.add_trace(go.Bar(name='graph size',
                         x=[str(a) for a in df_cats_for_means['similarity_community']],
                         y=df_cats_for_means['graph_size'],
                         text=df_cats_for_means['graph_size'],
                         textposition='auto',
                         texttemplate="%{y:.2f}",
                         width=[.5 for _ in range(len(df_cats_for_means['graph_size_ratio']))]
                         ),
                  row=1, col=1)
    fig.add_hline(y=df_cats_for_means['graph_size'].mean(), line_color='Grey', line_dash='dash', row=1, col=1)
    fig.add_trace(go.Bar(name='central graph size',
                         x=[str(a) for a in df_cats_for_means['similarity_community']],
                         y=df_cats_for_means['central_graph_size'],
                         text=df_cats_for_means['central_graph_size'],
                         textposition='auto',
                         texttemplate="%{y:.2f}",
                         width=[.5 for _ in range(len(df_cats_for_means['graph_size_ratio']))]
                         ),
                  row=1, col=2)
    fig.add_hline(y=df_cats_for_means['central_graph_size'].mean(), line_color='Grey', line_dash='dash', row=1, col=2)
    fig.add_trace(go.Bar(name='ratio',
                         x=[str(a) for a in df_cats_for_means['similarity_community']],
                         y=df_cats_for_means['graph_size_ratio'],
                         text=df_cats_for_means['graph_size_ratio'],
                         textposition='auto',
                         texttemplate="%{y:.2f}",
                         width=[.5 for _ in range(len(df_cats_for_means['graph_size_ratio']))]
                         ),
                  row=1, col=3)
    # fig.add_trace(go.Bar(name='fluidity total',
    #                      x=[str(a) for a in df_cats_for_means['similarity_community']],
    #                      y=df_cats_for_means['fluidity_total'],
    #                      text=df_cats_for_means['fluidity_total'],
    #                      textposition='auto',
    #                      texttemplate="%{y:.2f}",
    #                      ),
    #               row=2, col=2)
    # fig.add_trace(go.Bar(name='fluidity central',
    #                      x=[str(a) for a in df_cats_for_means['similarity_community']],
    #                      y=df_cats_for_means['fluidity_central'],
    #                      text=df_cats_for_means['fluidity_central'],
    #                      textposition='auto',
    #                      texttemplate="%{y:.2f}"
    #                      ),
    #               row=3, col=2)

    fig.add_hline(y=df_cats_for_means['graph_size_ratio'].mean(), line_color='Grey', line_dash='dash', row=1, col=3)
    fig.update_yaxes(title_text="graph size", showticklabels=False, row=1, col=1)
    fig.update_yaxes(title_text="central graph size", showticklabels=False, row=1, col=2)
    fig.update_yaxes(title_text="ratio", showticklabels=False, row=1, col=3)
    # fig.update_yaxes(title_text="fluidity total", showticklabels=False, row=2, col=2)
    # fig.update_yaxes(title_text="fluidity central", showticklabels=False, row=3, col=2)

    fig.update_layout(
        font=dict(
            size=10
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(zeroline=True, zerolinecolor='LightGrey', zerolinewidth=.1, showline=True, linecolor='Grey',
                     showgrid=True, gridwidth=.1, gridcolor='LightGrey')
    fig.update_xaxes(showline=True, linecolor='Grey')

    # fig.update_layout(height=750, width=750)
    fig.write_image("./images/graph_size_for_similarity_commmunity.pdf")

    return fig


# ----------------------------- similarity_category_plain ------------------------------------
def similarity_category_plain():
    df_similarity_category = df[(df.similarity_community == 21) | (df.similarity_community == 17)]
    df_similarity_category = df_similarity_category.groupby(
        ['similarity_community', 'category_community']).size().reset_index(name='counts')

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=df_similarity_category[(df_similarity_category.similarity_community == 21) & (
            df_similarity_category.category_community != -1)].category_community.values,
                         values=df_similarity_category[(df_similarity_category.similarity_community == 21) & (
                                 df_similarity_category.category_community != -1)].counts.values,
                         name="single"),
                  1, 1)
    fig.add_trace(go.Pie(labels=df_similarity_category[(df_similarity_category.similarity_community == 17) & (
            df_similarity_category.category_community != -1)].category_community.values,
                         values=df_similarity_category[(df_similarity_category.similarity_community == 17) & (
                                 df_similarity_category.category_community != -1)].counts.values,
                         name="multiple"),
                  1, 2)
    fig.update_traces(hole=.4, hoverinfo="label+percent+name", textinfo='none')
    fig.update_layout(
        showlegend=False,
        # title_text="Category Community for books in each main character similarity main sub",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='single', x=0.20, y=0.5, font_size=10, showarrow=False),
                     dict(text='multiple', x=0.80, y=0.5, font_size=10, showarrow=False)])
    return fig


# --------------------------------- similarity
def category_community_counts():
    fig = px.bar(x=[str(a) for a in df[df.category_community != -1].groupby(['category_community']).size().reset_index(
        name='counts').sort_values(by='counts', ascending=False)['category_community']],
                 y=df[df.category_community != -1].groupby(['category_community']).size().reset_index(
                     name='counts').sort_values(by='counts', ascending=False)['counts'])
    fig.update_yaxes(title='count')
    fig.update_xaxes(title='category community')
    fig.update_layout(
        font=dict(
            size=6
        ))
    return fig


def category_similarity_counts():
    df_similarity_category = df[(df.similarity_community == 21) | (df.similarity_community == 17)]
    df_similarity_category = df_similarity_category[(df_similarity_category.category_community != -1)]
    df_similarity_category = \
        df_similarity_category.groupby(['similarity_community', 'category_community']).size().reset_index(name='counts')
    df_similarity_category['sum_category_counts'] = \
        df_similarity_category.groupby(['category_community'])['counts'].transform('sum')
    df_similarity_category['ratio'] = df_similarity_category['counts'] / df_similarity_category['sum_category_counts']
    df_similarity_category = df_similarity_category.sort_values(by='ratio', ascending=False)
    df_similarity_category = df_similarity_category[df_similarity_category.sum_category_counts > 15]
    fig = go.Figure()
    fig.add_bar(name='single', x=[str(a) for a in df_similarity_category[
        df_similarity_category.similarity_community == 21].category_community.values],
                y=df_similarity_category[df_similarity_category.similarity_community == 21].counts.values /
                  df_similarity_category[df_similarity_category.similarity_community == 21].sum_category_counts.values)
    fig.add_bar(name='multiple', x=[str(a) for a in df_similarity_category[
        df_similarity_category.similarity_community == 17].category_community.values],
                y=df_similarity_category[df_similarity_category.similarity_community == 17].counts.values /
                  df_similarity_category[df_similarity_category.similarity_community == 17].sum_category_counts.values)
    fig.update_layout(barmode="stack")
    fig.update_yaxes(title='relative frequency')
    fig.update_xaxes(title='category community')
    fig.update_layout(
        font=dict(
            size=6
        ))
    return fig


def author_similarity_counts():
    df_similarity_author = df[(df.similarity_community == 21) | (df.similarity_community == 17)]
    # df_similarity_author = RelationAnalyses.get_rows_with_list_key_values(df_similarity_author, 'subjects_list_separated', ['Fiction'])
    df_similarity_author = \
        df_similarity_author.groupby(['similarity_community', 'author']).size().reset_index(name='counts')
    df_similarity_author['sum_author_counts'] = \
        df_similarity_author.groupby(['author'])['counts'].transform('sum')
    df_similarity_author['ratio'] = df_similarity_author['counts'] / df_similarity_author['sum_author_counts']
    df_similarity_author = df_similarity_author.sort_values(by='ratio', ascending=False)
    df_similarity_author = df_similarity_author[df_similarity_author.sum_author_counts > 0]
    fig = go.Figure()
    fig.add_bar(name='single', x=[str(a) for a in df_similarity_author[
        df_similarity_author.similarity_community == 21].author.values],
                y=df_similarity_author[df_similarity_author.similarity_community == 21].counts.values /
                  df_similarity_author[df_similarity_author.similarity_community == 21].sum_author_counts.values)
    fig.add_bar(name='multiple', x=[str(a) for a in df_similarity_author[
        df_similarity_author.similarity_community == 17].author.values],
                y=df_similarity_author[df_similarity_author.similarity_community == 17].counts.values /
                  df_similarity_author[df_similarity_author.similarity_community == 17].sum_author_counts.values)
    fig.update_layout(barmode="stack")
    fig.update_layout(
        font=dict(
            size=6
        ))
    fig.update_yaxes(title='relative frequency')
    fig.update_xaxes(title='authors with more than 15 books')
    return fig


# ---------------------------------


def graph_size_box_plots():
    # can make them Violin add Violin and remove box...
    df_size = df[(df.graph_size > 0)
                 & (df.central_graph_size > -1)
                 & (df.central_graph_size <= 400)].copy()
    fig = make_subplots(rows=1, cols=3)
    fig.add_trace(go.Box(
        y=df_size.graph_size.values,
        name='graph size',
        marker_color='#FF4136',
        boxmean='sd',  # represent mean and standard deviation
        boxpoints='all',
        hovertext=df_size.name,
        jitter=0.3,
        marker_size=2,
        line_width=1
    ), col=1, row=1)
    fig.add_trace(go.Box(
        y=df_size.central_graph_size.values,
        name='central graph size',
        marker_color='#FF851B',
        boxmean='sd',  # represent mean and standard deviation
        boxpoints='all',
        hovertext=df_size.name,
        jitter=0.3,
        marker_size=2,
        line_width=1
    ), col=2, row=1)
    fig.add_trace(go.Box(
        y=df_size.graph_size_ratio.values,
        name='graph size ratio',
        marker_color='#3D9970',
        boxmean='sd',  # represent mean and standard deviation
        boxpoints='all',
        hovertext=df_size.name,
        jitter=0.3,
        marker_size=2,
        line_width=1
    ), col=3, row=1)
    fig.update_layout(
        font=dict(
            size=10
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(zeroline=True, zerolinecolor='LightGrey', zerolinewidth=.1, showline=True, linecolor='Grey',
                     showgrid=True, gridwidth=.1, gridcolor='LightGrey')
    fig.update_xaxes(showline=True, linecolor='Grey')
    fig.write_image("./images/graph_size_box_plots.pdf")
    return fig


def author_book_counts():
    a0 = len(RelationAnalyses.select_repeated(df, 'author', 0).value_counts('author'))
    a1 = len(RelationAnalyses.select_repeated(df, 'author', 15).value_counts('author'))
    a2 = len(RelationAnalyses.select_repeated(df, 'author', 30).value_counts('author'))
    a3 = len(RelationAnalyses.select_repeated(df, 'author', 45).value_counts('author'))
    a4 = len(RelationAnalyses.select_repeated(df, 'author', 60).value_counts('author'))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['<15', '15-30', '30-45', '45-60', '>60'],
                         y=[a0 - a1, a1 - a2, a2 - a3, a3 - a4, a4],
                         text=[a0 - a1, a1 - a2, a2 - a3, a3 - a4, a4],
                         textposition='auto',
                         texttemplate="%{y:.2f}"
                         ))
    fig.update_yaxes(title_text='number of authors', showticklabels=False)
    fig.update_xaxes(title_text='number of books')
    fig.update_layout(
        font=dict(
            size=10
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(zeroline=True, zerolinecolor='LightGrey', zerolinewidth=.1, showline=True, linecolor='Grey',
                     showgrid=True, gridwidth=.1, gridcolor='white')
    fig.update_xaxes(showline=True, linecolor='Grey')
    fig.write_image("./images/author_book_counts.pdf")
    return fig


# ------------------ graph size distributions
def graph_size_distributions():
    fig = make_subplots(rows=1, cols=3)
    df_temp = df[
            (df.graph_size > 0)
             & (df.central_graph_size > -1)
             & (df.central_graph_size <= 400)
             ]
    fig.add_trace(go.Histogram(
        x=df_temp.graph_size.values,
        name='graph size',
        marker_color='#FF4136',
        # marginal="rug"
    ), col=1, row=1)
    fig.add_trace(go.Histogram(
        x=df_temp.central_graph_size.values,
        name='central graph size',
        marker_color='#FF851B',
    ), col=2, row=1)
    fig.add_trace(go.Histogram(
        x=df_temp.graph_size_ratio.values,
        name='graph size ratio',
        marker_color='#3D9970',
    ), col=3, row=1)
    fig.update_xaxes(title_text='graph size', row=1, col=1)
    fig.update_xaxes(title_text='central graph size', row=1, col=2)
    fig.update_xaxes(title_text='ratio', row=1, col=3)
    fig.update_yaxes(title_text='count', row=1, col=1)
    fig.update_layout(
        font=dict(
            size=10
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(zeroline=True, zerolinecolor='LightGrey', zerolinewidth=.1, showline=True, linecolor='Grey',
                     showgrid=True, gridwidth=.1, gridcolor='White')
    fig.update_xaxes(showline=True, linecolor='Grey')
    fig.write_image("./images/graph_size_distributions.pdf")
    fig.show()

