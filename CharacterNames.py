import os
import nltk
from nameparser.parser import HumanName
import networkx as nx


# TODO Improve the similarity condition
# TODO Improve names extraction: Try stanford for names extraction
# TODO Names with size 1 or less are IGNORED now!


def get_human_names(text):
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


def test_A_Christmas_Carol_Names():
    book_address = "./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt"
    book_read = open(book_address, "r")
    # whole book as a string
    lis = book_read.readlines()
    stri = ""
    for i in range(len(lis)):
        stri = stri + lis[i]
    names = get_human_names(stri)

    print("LAST, FIRST")
    for name in names:
        last_first = HumanName(name).last + ', ' + HumanName(name).first
        print(last_first)


def test_A_Christmas_Carol_Graph():
    book_address = "./Data/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt"
    book_read = open(book_address, "r")
    # whole book as a string
    stri = ""
    people = []
    graph = nx.Graph()
    for li, line in enumerate(book_read.readlines()):
        stri = stri + line
        if li % 30 == 1:
            names = get_human_names(stri)
            for name in names:
                if name not in people:
                    people.append(name)
                    graph.add_node(len(people))
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    ind_i = people.index(names[i])
                    ind_j = people.index(names[j])
                    graph.add_edge(ind_i, ind_j)
            stri = ""
    return people, graph


def visualize_graph(people, graph):
    print("not implemented")


if __name__ == '__main__':
    test_A_Christmas_Carol_Graph()
