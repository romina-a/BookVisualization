import os
import nltk
from nameparser.parser import HumanName
import networkx as nx
from nltk.tag import StanfordNERTagger
import spacy
import os
import stanza
from nltk.parse import CoreNLPParser


# ~~~~~~~~~~~~~~~~~~~~~~~~~Name Extraction Methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TODO force include prefixes with condition in get names(if last word is Mrs or ... )

def get_character_names_nltk(text):
    """
    :param text: raw text
    :return: list of strings of all names (repetitions are not removed)
    """
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
    person = []
    person_list = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        for part in person:
            name += part + ' '
        person_list.append(name[:-1])
        name = ''
        person = []
    return person_list


def get_character_names_spacy(text):  # using spacy
    """
        :param text: raw text
        :return: list of strings of all names (repetitions are not removed)
    """
    # Create Doc object
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Identify the persons
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

    # Return persons
    return persons


def get_character_names_stanford(text, PATH="./stanford-ner"):  # using stanford
    """
    :param text: raw text
    :param PATH: path to stanford-ner folder
    :return: list of strings of all names (repetitions are not removed)
    """

    # Path to stanford-ner folder
    CLASSIFIER_PATH = os.path.join(PATH, "classifiers/english.all.3class.distsim.crf.ser.gz")
    JAR_PATH = os.path.join(PATH, "stanford-ner.jar")
    st = StanfordNERTagger(CLASSIFIER_PATH, JAR_PATH)

    tokens = nltk.tokenize.word_tokenize(text)
    wtags = st.tag(tokens)
    person_list = []
    name = ""
    for (w, t) in wtags:
        if t == 'PERSON':
            name = name + w + " "
        else:
            if name != "":
                person_list.append(name[:-1])
                name = ""
    return person_list


def get_character_names_stanford_server(text):  # using stanford
    """
    MUST have the Stanford CoreNLP server running
    NOTE source: https://github.com/nltk/nltk/wiki/Stanford-CoreNLP-API-in-NLTK
    :param text: raw text
    :return: list of strings of all names (repetitions are not removed)
    """
    if text.isspace():
        return []
    # print("text:", text)
    SERVER_URL = 'http://localhost:9000'
    tokenizer = CoreNLPParser(url=SERVER_URL)
    ner_tagger = CoreNLPParser(url=SERVER_URL, tagtype='ner')
    tokens = tokenizer.tokenize(text)
    wtags = ner_tagger.tag(tokens)
    person_list = []
    name = ""
    for (w, t) in wtags:
        if t == 'PERSON':
            name = name + w + " "
        else:
            if name != "":
                person_list.append(name[:-1])
                name = ""
    # print("people:", person_list)
    return person_list


def get_character_names_stanza_OntoNotes(text):
    """
    to download the model:
        stanza.download('en')
    :param text: raw text
    :return: list of strings of all names (repetitions are not removed)
    """
    nlp = stanza.Pipeline('en', verbose=False)
    doc = nlp(text)
    persons = [ent.text for ent in doc.entities if ent.type == 'PERSON']
    return persons


def get_character_names_stanza_CoNLL03(text):
    """
    to download the model:
        stanza.download('en')
        stanza.download('en', processors={'ner': 'CoNLL03'})
    :param text: raw text
    :return: list of strings of all names (repetitions are not removed)
    """
    nlp = stanza.Pipeline('en', verbose=False, processors={'ner': 'CoNLL03'})
    doc = nlp(text)
    persons = [ent.text for ent in doc.entities if ent.type == 'PER']
    return persons


# ~~~~~~~~~~~~~~~~~~~~~~~~~Graph creation~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# !!! Deprecated
def create_character_graph(book_address, max_dist=30):
    """
    :param max_dist: distance between two words (#sentences) determining a relation (i.e. a page)
    :param book_address:
    :return graph: networkx wieghted graph, nodes are labeled 0, 1, ...
    :return names: list of node names, names[i] = name of node i in the graph.
    :return counts: number of each name's appearances in the text, name[i] is found count[i] times
    """
    book_read = open(book_address, "r")
    last_line_ind = len(book_read.readlines()) - 1
    book_read = open(book_address, "r")

    # whole book as a string
    stri = ""
    names = []
    counts = []
    G = nx.Graph()
    cashed_names = []
    for li, line in enumerate(book_read.readlines()):
        stri = stri + line
        if li % (max_dist // 2) == 1 or li ==last_line_ind:
            new_names = get_character_names_stanford_server(stri)  # NOTE: the name extractor

            # # remove repeated names
            # new_names = list(set(new_names))

            # add new names to list of all names
            for name in new_names:
                if name not in names:
                    names.append(name)
                    counts.append(1)
                    G.add_node(names.index(name))
                else:
                    counts[names.index(name)] += 1
            # draw edges
            for i in range(len(new_names)):
                # adding rels between all newly seen
                for j in range(i + 1, len(new_names)):
                    ind_i = names.index(new_names[i])
                    ind_j = names.index(new_names[j])
                    if G.has_edge(ind_i, ind_j):
                        G[ind_i][ind_j]["weight"] += 1
                    else:
                        G.add_edge(ind_i, ind_j, weight=1)
                # adding rels between newly seen and previously seen
                for s in cashed_names:
                    ind_i = names.index(new_names[i])
                    ind_j = names.index(s)
                    if G.has_edge(ind_i, ind_j):
                        G[ind_i][ind_j]["weight"] += 1
                    else:
                        G.add_edge(ind_i, ind_j, weight=1)
            cashed_names = new_names
            stri = ""
    return G, names, counts


def _draw_edges(G, new_names, cashed_names, li):
    """
    1. Draws edges between every two words in new_names.
    2. Draws edges between all words in cashed_names and all words in new_names
    :param G: Graph
    :param new_names: list of strings
    :param cashed_names: list of strings
    :param li: int, the time stamp
    """
    for i in range(len(new_names)):
        # adding rels between all newly seen
        for j in range(i + 1, len(new_names)):
            u = new_names[i]
            v = new_names[j]
            G.add_edge(u, v, time=li)
        # adding rels between newly seen and previously seen
        for j in range(len(cashed_names)):
            u = new_names[i]
            v = cashed_names[j]
            G.add_edge(u, v, time=li)


def create_character_MultiGraph(book_address, max_dist=30):
    """
    :param max_dist: distance between two words (#sentences) determining a relation (i.e. a page)
    :param book_address:
    :return graph: networkx MultiGraph, node labels are character names. Each
    """
    book_read = open(book_address, "r")
    last_line_ind = len(book_read.readlines()) - 1
    book_read = open(book_address, "r")
    # whole book as a string
    stri = ""
    G = nx.MultiGraph()
    cashed_names = []

    for li, line in enumerate(book_read.readlines()):
        stri = stri + line
        if li % (max_dist // 2) == (max_dist // 2) - 1 or li == last_line_ind:
            print(f"{((li*100)//last_line_ind)}% done", end='\r')
            new_names = get_character_names_stanford_server(stri)  # NOTE: the name extractor

            # add new names to list of all names and increase count
            for name in new_names:
                if not G.has_node(name):
                    G.add_node(name)
                    G.nodes[name]['count'] = 1
                else:
                    G.nodes[name]['count'] += 1

            # # remove repeated names
            # new_names = list(set(new_names))

            _draw_edges(G, new_names, cashed_names, li)

            cashed_names = new_names
            stri = ""
    return G


# ~~~~~~~~~~~~~~~~~~~~~~~~~Graph post processing~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TODO this is simple, improve
def _names_similar(name1, name2):
    """
    :param name1: string
    :param name2: string
    :return: true if strings are the same person
    """
    # if no similar words between the names
    if len(set(name1.split()).intersection(set(name2.split()))) == 0:
        return False

    hn1 = HumanName(name1.lower())
    hn2 = HumanName(name2.lower())

    # if both names have first and last and at least one does not match return False
    if hn1.first !='' and hn2.first !='' and hn1.last!='' and hn2.last!='':
        return hn1.first == hn2.first and hn1.last == hn2.last

    if hn1.first != '' and hn2.first != '' and hn1.first != hn2.first:
        return False
    if hn1.last != '' and hn2.last != '' and hn1.last != hn2.last:
        return False
    if hn1.title in ['Mrs.'] and hn2.title in ['Ms.', 'Miss']:
        return False
    if hn2.title in ['Mrs.'] and hn1.title in ['Ms.', 'Miss']:
        return False
    return True


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

    # if the titles exist and genders dont match return True
    if hn1.title in ['Mrs.'] and hn2.title in ['Ms.', 'Miss']:
        return True
    if hn2.title in ['Mrs.'] and hn1.title in ['Ms.', 'Miss']:
        return True

    # otherwise no conflict
    return False


def _merge_nodes(G, nodes):
    """
    Merges the nodes, the resulting node's name is the name with the most count
    :param G: networkx MultiGraph whose nodes will be merged
    :param nodes: list of node ids of G to be merged
    """
    main = max(nodes, key=lambda x: G.nodes[x]['count'])
    for n in nodes:
        if n == main: continue
        G.nodes[main]['count'] += G.nodes[n]['count']
        nx.contracted_nodes(G, main, n, self_loops=False, copy=False)


# TODO can make better, now removes the minimum number of edges to have zero conflicts
def _clear_conflicts(G_sim):
    for c in nx.connected_components(G_sim):
        for name1 in c:
            for name2 in c:
                if _names_conflict(name1, name2):
                    edges = nx.connectivity.minimum_st_edge_cut(G_sim, name1, name2)
                    for e in edges:
                        G_sim.remove_edge(e[0], e[1])


def _similarity_graph(G):
    G_sim = nx.Graph()
    for n in G.nodes():
        G_sim.add_node(n)
    for u in list(G):
        for v in list(G):
            if _names_similar(u, v) and u != v:
                G_sim.add_edge(u, v, c=1)
    for u in list(G):
        for v in list(G):
            if _names_similar(u, v) and u != v:
                G_sim.add_edge(u, v, c=1)
    return G_sim


def merge_similar_nodes(G):
    sim = _similarity_graph(G)
    _clear_conflicts(sim)
    con_comps = nx.connected_components(sim)
    con_comps_list = []
    for c in con_comps:
        con_comps_list.append(list(c))
    for c in con_comps_list:
        _merge_nodes(G, c)
