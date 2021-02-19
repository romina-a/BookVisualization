import os
import nltk
from nameparser.parser import HumanName
import networkx as nx


# TODO Improve the similarity condition
# TODO Improve names extraction: Try stanford for names extraction
# TODO Names with size 1 or less are IGNORED in get_character_names


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
        for part in person:
            name += part + ' '
        if name[:-1] not in person_list:
            person_list.append(name[:-1])
        name = ''
        person = []
    return person_list


def print_character_names(book_address):
    """
    prints all characters' name and last name found in the book
    """
    book_read = open(book_address, "r")
    # whole book as a string
    lis = book_read.readlines()
    stri = ""
    for i in range(len(lis)):
        stri = stri + lis[i]

    names = get_character_names_v2(stri)
    print("LAST, FIRST")
    for name in names:
        last_first = HumanName(name).last + ', ' + HumanName(name).first
        print(last_first)


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
    graph = nx.Graph()
    for li, line in enumerate(book_read.readlines()):
        stri = stri + line
        if li % 30 == 1:
            new_names = get_character_names_v2(stri)
            for name in new_names:
                if name not in names:  # TODO for loop and check the name exists or not
                    names.append(name)
                    counts.append(1)
                    graph.add_node(names.index(name))
                else:
                    counts[names.index(name)] += 1
            for i in range(len(new_names)):
                for j in range(i + 1, len(new_names)):
                    ind_i = names.index(new_names[i])
                    ind_j = names.index(new_names[j])
                    graph.add_edge(ind_i, ind_j)
            stri = ""
    return graph, names, counts


if __name__ == '__main__':
    create_character_graph(book_address="./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt")
