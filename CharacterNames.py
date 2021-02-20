import os
import nltk
from nameparser.parser import HumanName
import networkx as nx
from nltk.tag import StanfordNERTagger
import os


# TODO Improve the similarity condition
# TODO Improve names extraction: Try stanford for names extraction
# TODO Names with size 1 or less are IGNORED in get_character_names

# Deprecated!
def get_character_names(text):
    """
    :param text: raw text
    :return: list of strings of all names
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
        if len(person) > 1:  # avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
        name = ''
        person = []
    return person_list


def get_character_names_v2(text):
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
        if name[:-1] not in person_list:  # TODO remove this if and handle the case in the caller
            person_list.append(name[:-1])
        name = ''
        person = []
    return person_list


def get_character_names_stanford(text, PATH = "./stanford-ner"):
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


def names_similar(name1, name2):
    """
    :param name1: string
    :param name2: string
    :return: true if strings are the same person
    """
    hn1 = HumanName(name1)
    hn2 = HumanName(name2)
    if len(hn1) == len(hn2):
        return hn1 == hn2
    else:
        return name1 in name2 or name2 in name1


def name_in_list(name, nlist, scores):
    """
    :param name: string
    :param nlist: list of strings
    :param scores: score of each name, if two similar names are found, the one with higher score is returned
    :return: if name exists: index of name in nlist, else None
    """
    index = None
    s = min(scores)
    for i, n in enumerate(nlist):
        if names_similar(name, n):
            if scores[i] >= s:
                s = scores[i]
                index = i
    return index


def update_name_in_list(name, nlist, index):
    if len(HumanName(name)) > len(HumanName(nlist[index])):
        nlist[index] = name


# TODO Clean the graph before outputting
def create_character_graph(book_address):
    """
    :param book_address:
    :return graph: networkx graph, nodes are labeled 0, 1, ...
    :return names: list of node names, names[i] = name of node i in the graph.
    :return counts: number of each name's appearance in the text, name[i] is found count[i] times
    """
    book_read = open(book_address, "r")
    # whole book as a string
    stri = ""
    names = []
    counts = []
    G = nx.Graph()
    for li, line in enumerate(book_read.readlines()):
        stri = stri + line
        if li % 10 == 1:
            new_names = get_character_names_v3(stri)  # NOTE: the name extractor
            for name in new_names:
                if name not in names:  # TODO for loop and check the name exists or not?
                    names.append(name)
                    counts.append(1)
                    G.add_node(names.index(name))
                else:
                    counts[names.index(name)] += 1
            for i in range(len(new_names)):
                for j in range(i + 1, len(new_names)):
                    ind_i = names.index(new_names[i])
                    ind_j = names.index(new_names[j])
                    if G.has_edge(ind_i, ind_j):
                        G[ind_i][ind_j]["weight"] += 1
                    else:
                        G.add_edge(ind_i, ind_j, weight=1)
            stri = ""
    return G, names, counts


if __name__ == '__main__':
    create_character_graph(book_address="./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt")

