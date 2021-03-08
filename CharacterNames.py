from nameparser.parser import HumanName
import networkx as nx
from ExtractNames import get_character_names_stanford_server as extract_names
import os

MAX_DIST_DEFAULT = 10

# This is the layout for drawing the graphs.
# It sit set here, because if we set it when we want to draw the graph, each time it changes
# and the snapshots will not be visualized the way we want (with nodes in fixed positions)
LAYOUT_DEFAULT = 'kamada_kawai'

layout_options = {
    'spring': nx.spring_layout,
    'circular': nx.circular_layout,
    'kamada_kawai': nx.kamada_kawai_layout,
    'shell': nx.shell_layout,
}


def set_layout(G, layout):
    """
    Sets 'pos' attribute on G nodes based on the layout.

    :param G: nx Graph of any type
    :param layout: string, options: 'spring','circular','kamada_kawai','shell'
    """
    pos = layout_options[layout](G)
    nx.set_node_attributes(G, pos, 'pos')


# ~~~~~~~~~~~~~~~~~~~~~~~~~ Helper ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extract_book_name_from_adr(adr):
    file_name = os.path.split(adr)[-1]
    name = os.path.splitext(file_name)[0]
    return name


# ~~~~~~~~~~~~~~~~~~~~~~~~~Graph creation~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TODO ? add 'times': list of ints, all the times the character name was seen. len(times)=count
#  must change: create_character_MultiGraph, and _merge_nodes_in_MultiGraph
def _draw_edges(G, new_names, cashed_names, time_stamp):
    """
    Draws edges between input lists (details: ↓), each edge has attribute 'time':time_stamp
    1. Draws edges between every two words in new_names.
    2. Draws edges between all words in cashed_names and all words in new_names

    :param G: nx.MultiGraph
    :param new_names: list of strings
    :param cashed_names: list of strings
    :param time_stamp: int, the time stamp
    """
    for i in range(len(new_names)):
        # adding edges between all newly seen
        for j in range(i + 1, len(new_names)):
            u = new_names[i]
            v = new_names[j]
            if u == v: continue
            G.add_edge(u, v, time=time_stamp)
        # adding edges between newly seen and previously seen
        for j in range(len(cashed_names)):
            u = new_names[i]
            v = cashed_names[j]
            if u == v: continue
            G.add_edge(u, v, time=time_stamp)


def create_character_MultiGraph(book_address, max_dist=MAX_DIST_DEFAULT, layout=LAYOUT_DEFAULT):
    """
    returns an nx.MultiGraph (https://networkx.org/documentation/stable/reference/classes/multigraph.html)
    with the following properties:
            -graph attributes (G.graph()):
                             'end_time': int, the last time_stamp
            each node id is a unique character name
            -node attributes (G.nodes(data=True)[<node_id>]):
                             'count': int, total #times the character name was found in the book
                             'times': list of int (sorted), each time the node appears
                             'pos': tuple, (x,y) set based on the layout. For drawing.
            -edge attributes (G.edges(data=True)[<u_id>,<v_id>, key]]/G.get_edge_data(<u_id>,<v_id>)):
                             'time': time stamps representing when u and v appeared closer than max_dist

    :param max_dist: int, distance between two words (#sentences) determining a relation (i.e. a page)
    :param book_address: string, the address to .txt file of the book
    :param layout: string, options: 'spring','circular','kamada_kawai','shell'
    :return graph: nx.MultiGraph
    """
    book_read = open(book_address, "r")
    last_line_ind = len(book_read.readlines()) - 1
    book_read = open(book_address, "r")

    # whole book as a string
    text = ""
    G = nx.MultiGraph()
    cashed_names = []
    time = 0
    for line_number, line in enumerate(book_read.readlines()):
        text = text + line
        if line_number % (max_dist // 2) == (max_dist // 2) - 1 or line_number == last_line_ind:
            print(f"{((line_number * 100) // last_line_ind)}% done", end='\r')
            new_names = extract_names(text)  # NOTE: the name extractor

            # add new names to list of all names and increase count
            for name in new_names:
                if not G.has_node(name):
                    G.add_node(name)
                    G.nodes[name]['count'] = 1
                    G.nodes[name]['times'] = [time]
                else:
                    G.nodes[name]['count'] += 1
                    G.nodes[name]['times'].append(time)

            _draw_edges(G, new_names, cashed_names, time)
            time += 1

            cashed_names = new_names
            text = ""
    G.graph['end_time'] = time
    G.graph['name'] = extract_book_name_from_adr(book_address)
    set_layout(G, layout)
    return G


# ~~~~~~~~~~~~~~~~~~~~~~~~~Graph post processing~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def _names_similar(name1, name2):
    """
    gets two names and returns True if they (probably) represent the same person
    :param name1: string
    :param name2: string
    :return: true if strings are the same person
    """
    name1_lower_list = name1.lower().split()
    name2_lower_list = name2.lower().split()
    # if no similar words between the names
    if len([common for common in name1_lower_list if common in name2_lower_list]) == 0:
        return False
    # subsets

    #TODO: Sadegh Kaveh = Kaveh Sadegh which is wrong
    if len(set(name1_lower_list).intersection(set(name2_lower_list))) == len(name1_lower_list):
        return True
    if len(set(name1_lower_list).intersection(set(name2_lower_list))) == len(name2_lower_list):
        return True
    # titles!
    hn1 = HumanName(name1.lower())
    hn2 = HumanName(name2.lower())
    # {title} first= & last=
    if hn1.first != '' and hn2.first != '' and hn1.last != '' and hn2.last != '':
        return hn1.first == hn2.first and hn1.last == hn2.last
    # {title} first! & {last}
    if hn1.first != '' and hn2.first != '' and hn1.first != hn2.first:
        return False
    # {title} {first} & last!
    if hn1.last != '' and hn2.last != '' and hn1.last != hn2.last:
        return False
    # title
    if hn1.title in ['mrs.'] and hn2.title in ['ms.', 'miss']:
        return False
    if hn2.title in ['mrs.'] and hn1.title in ['ms.', 'miss']:
        return False
    # title - honorifics - kinship
    if hn1.title in ['mr.', 'sir', 'uncle', "master",
                     "gentleman", "sire", "dad", "father",
                     "grandpa", "lord", "brother",
                     "nephew", "king", "prince"] and \
            hn2.title in ['ms.', 'miss', "mrs.",
                          "mistress", "madam", "madame", "maam",
                          "mom", "mother", "grandma", "granny", "dame", "lady",
                          "sister", "niece", "queen", "princess"]:
        return False
    if hn2.title in ['mr.', 'sir', 'uncle',
                     "master", "gentleman", "sire",
                     "dad", "father", "grandpa",
                     "lord", "brother",
                     "nephew", "king", "prince"] and \
            hn1.title in ['ms.', 'miss', "mrs.",
                          "mistress", "madam", "madame", "maam",
                          "mom", "mother", "grandma", "granny", "dame", "lady",
                          "sister", "niece", "queen", "princess"]:
        return False
    return True


# TODO is this correct? why two similar for loops?
def _name_similarity_graph(G):
    """
    uses _names_similar to check similarity

    :param G: nx.MultiGraph,
    :return: nx.Graph, nodes ids are the same as G,
                       connected nodes are (probably) similar
    """
    G_sim = nx.Graph()
    for n in G.nodes():
        G_sim.add_node(n)
    for u in list(G):
        for v in list(G):
            if _names_similar(u, v) and u != v:
                G_sim.add_edge(u, v, c=1)
    # for u in list(G):
    #     for v in list(G):
    #         if _names_similar(u, v) and u != v:
    #             G_sim.add_edge(u, v, c=1)
    return G_sim


def _names_conflict(name1, name2):
    """
    returns True if the two words CANNOT be the same person
       :param name1: string
       :param name2: string
       :return: true if strings can not be the same person
    """

    hn1 = HumanName(name1.lower())
    hn2 = HumanName(name2.lower())

    # if both names have first and last and at least one does not match return True
    if hn1.first != '' and hn2.first != '' and hn1.last != '' and hn2.last != '':
        return not (hn1.first == hn2.first and hn1.last == hn2.last)
    # title
    if hn1.title in ['mrs.'] and hn2.title in ['ms.', 'miss']:
        return True
    if hn2.title in ['mrs.'] and hn1.title in ['ms.', 'miss']:
        return True
    # title - honorifics - kinship
    if hn1.title in ['mr.', 'sir', 'uncle', "master",
                     "gentleman", "sire", "dad", "father",
                     "grandpa", "lord", "brother",
                     "nephew", "king", "prince"] and \
            hn2.title in ['ms.', 'miss', "mrs.",
                          "mistress", "madam", "madame", "maam",
                          "mom", "mother", "grandma", "granny", "dame", "lady",
                          "sister", "niece", "queen", "princess"]:
        return True
    if hn2.title in ['mr.', 'sir', 'uncle',
                     "master", "gentleman", "sire",
                     "dad", "father", "grandpa",
                     "lord", "brother",
                     "nephew", "king", "prince"] and \
            hn1.title in ['ms.', 'miss', "mrs.",
                          "mistress", "madam", "madame", "maam",
                          "mom", "mother", "grandma", "granny", "dame", "lady",
                          "sister", "niece", "queen", "princess"]:
        return True

    # otherwise no conflict
    return False


# TODO think of other ways maybe, now removes the minimum number of edges to have zero conflicts
#  --> think about a way to consider all conflicts and then remove the minimum edges to solve them all
def _clear_name_conflicts(G_sim):
    """
    WARNING: changes G_sim
    for each connected component in G_sim, (the nodes that are grouped together),
        if there is a conflict between two of the nodes (using _names_conflict),
        removes the minimum number of edges to resolve the conflict, and continues.
        G_sim's connected components do not have conflicts.
        The resulting graph depends on the order of processing the nodes.
        The resulting graph is not the optimal solution.

    :param G_sim: nx.Graph
    """
    for c in nx.connected_components(G_sim):
        for name1 in c:
            for name2 in c:
                if _names_conflict(name1, name2):
                    edges = nx.connectivity.minimum_st_edge_cut(G_sim, name1, name2)
                    for e in edges:
                        G_sim.remove_edge(e[0], e[1])


def _merge_nodes_in_MultiGraph(G, nodes):
    """
    WARNING: Changes G
    Merges all the nodes,
    the resulting node's name is the name with the most count,
    all edges preserved

    :param G: nx.MultiGraph, its nodes will be merged
    :param nodes: list of strings, the node ids of G to be merged
    """
    main = max(nodes, key=lambda x: G.nodes[x]['count'])
    for n in nodes:
        if n == main: continue
        # Add merged nod info to main node info
        G.nodes[main]['count'] += G.nodes[n]['count']
        for i in G.nodes[n]['times']: G.nodes[main]['times'].append(i)
        G.nodes[main]['times'] = sorted(G.nodes[main]['times'])
        # merge nodes
        nx.contracted_nodes(G, main, n, self_loops=False, copy=False)


def merge_similar_nodes(G):
    """
    WARNING: Changes G
    Merges all nodes in G that are similar and are not conflicting.
    All edges and their data are preserved.
    If two nodes are merged, the resulting node's id is the id that has the most counts.
    If u and v are merged and the resulting node's id is u:
                1. u's attribute count will be the sum of u and v's count.
                2. node v and its attributes will be added as a new attribute to node u's attribute: 'contraction'
    :param G: mx.MultiGraph
    """
    sim = _name_similarity_graph(G)
    _clear_name_conflicts(sim)
    con_comps = nx.connected_components(sim)
    con_comps_list = []
    for c in con_comps:
        con_comps_list.append(list(c))
    for c in con_comps_list:
        _merge_nodes_in_MultiGraph(G, c)
