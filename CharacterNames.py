import os
import nltk
from nameparser.parser import HumanName
import networkx as nx
import spacy  # python -m spacy download en
import en_core_web_sm
from nltk.tag import StanfordNERTagger


# TODO Improve names extraction
# TODO Improve the similarity condition, Cleaning
# TODO Describing the link
# TODO Clean the graph before outputting


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


def filtering(text):
    text = text.replace("\t", " ")
    text = text.replace("\n", " ")
    text = text.replace("!", " ! ")
    text = text.replace(":", " : ")
    text = text.replace("Mr.", "Mr")
    text = text.replace("Ms.", "Ms")
    text = text.replace("Mrs.", "Mrs")
    text = text.replace(".", " . ")
    text = text.replace("?", " ? ")
    text = text.replace(")", " ) ")
    text = text.replace("(", " ( ")
    text = text.replace("'s", " ")
    text = text.replace('"', ' " ')
    text = text.replace("'", " ' ")
    text = text.replace("`", " ` ")
    text = text.replace(",", " , ")
    text = text.replace(";", " ; ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    return text


'''
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
        

def print_character_names(book_address):

    book_read = open(book_address, "r")
    # whole book as a string
    book_lines = book_read.readlines()
    text = ""
    for i in range(len(book_lines)):
        text = text + book_lines[i]

    names = get_character_names_spacy(text)
    print("FIRST LAST")
    for name in names:
        first_last = HumanName(name).first + ' ' + HumanName(name).last
        print(first_last)


def names_in_book(address="./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt"):
    book_read = open(address, "r")
    lines = book_read.readlines()
    text = ""
    for i in range(len(lines)):
        text = text + lines[i]
    book_read.close()
    names = get_character_names_spacy(text)
    return names
'''


def create_character_graph(book_address, max_dist=30):
    """
    :param max_dist: distance between two words (#sentences) determining a relation (i.e. a page)
    :param book_address:
    :return graph: networkx graph, nodes are labeled 0, 1, ...
    :return names: list of node names, names[i] = name of node i in the graph.
    :return counts: number of each name's appearances in the text, name[i] is found count[i] times
    """
    book_read = open(book_address, "r")
    # whole book as a string
    text = ""
    names = []
    counts = []
    G = nx.Graph()
    cashed_names = []
    for li, line in enumerate(book_read.readlines()):
        text = text + line
        if li % (max_dist//2) == 1:
            # filtering
            text = filtering(text)
            # the name extractor
            new_names = get_character_names_spacy(text)
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
            text = ""
    return G, names, counts


def create_character_graph_by_search(book_address, max_dist=30):
    """
    :param max_dist: distance between two words (#sentences) determining a relation (i.e. a page)
    :param book_address:
    :return graph: networkx graph, nodes are labeled 0, 1, ...
    :return names: list of node names, names[i] = name of node i in the graph.
    :return counts: number of each name's appearances in the text, name[i] is found count[i] times
    """
    book_read = open(book_address, "r")
    # whole book as a string
    text = ""
    names = []
    counts = []
    G = nx.Graph()
    cashed_names = []
    for li, line in enumerate(book_read.readlines()):
        text = text + line
        if li % (max_dist//2) == 1:
            # filtering
            text = filtering(text)
            # the name extractor
            available_names = get_character_names_spacy(text)
            # add new names to list of all names
            for name in available_names:
                if name not in names:
                    names.append(name)
                    counts.append(0)
                    G.add_node(names.index(name))
            # counts
            for name in names:
                res = [i for i in range(len(text)) if text.startswith(name, i)]
                counts[names.index(name)] += len(res)
                res.clear()
    print(5)
    text = ""
    for li, line in enumerate(book_read.readlines()):  # more accurate rather do them all in one loop
        text = text + line
        if li % (max_dist // 2) == 1:
            # filtering
            text = filtering(text)
            # available names in the paragraph
            available_names = [name for name in names if text.find(name) >= 0]
            # draw edges
            for i in range(len(available_names)):
                # adding rels between all newly seen
                for j in range(i + 1, len(available_names)):
                    ind_i = names.index(available_names[i])
                    ind_j = names.index(available_names[j])
                    if G.has_edge(ind_i, ind_j):
                        G[ind_i][ind_j]["weight"] += 1
                    else:
                        G.add_edge(ind_i, ind_j, weight=1)
                # adding rels between newly seen and previously seen
                for s in cashed_names:
                    ind_i = names.index(available_names[i])
                    ind_j = names.index(s)
                    if G.has_edge(ind_i, ind_j):
                        G[ind_i][ind_j]["weight"] += 1
                    else:
                        G.add_edge(ind_i, ind_j, weight=1)

            cashed_names = available_names
            text = ""
    return G, names, counts


if __name__ == '__main__':
    create_character_graph(book_address="./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt")
