import os
import nltk
from nameparser.parser import HumanName
import networkx as nx
import spacy  # python -m spacy download en
import en_core_web_sm


# TODO Improve names extraction: NLTK, Stanford, SpaCy, Google
# TODO Words in the first of the sentence
# TODO Improve the similarity condition
# TODO Cleaning SpaCy{}
# TODO Describing the link


def get_character_names(text):  # using nltk
    """
    :param text: raw text
    :return: list of strings of all names
    """
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sent = nltk.ne_chunk(pos, binary=False)
    person = []
    person_list = []
    name = ""
    for subtree in sent.subtrees(filter=lambda t: t.label() == 'PERSON'):
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


def get_character_names_v2(text):  # using nltk
    """
    :param text: raw text
    :return: list of strings of all names
    """
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sent = nltk.ne_chunk(pos, binary=False)
    person = []
    person_list = []
    name = ""
    for subtree in sent.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        for part in person:
            name += part + ' '
        if name[:-1] not in person_list:
            person_list.append(name[:-1])
        name = ''
        person = []
    return person_list


def get_character_names_v3(text):  # using spacy
    # Create Doc object
    nlp = en_core_web_sm.load()
    doc = nlp(text)

    # Identify the persons
    persons = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

    persons = similarity_filtering_names(persons)

    # Return persons
    return persons


def similarity_filtering_names(names):
    filtered_people = []
    nlp = en_core_web_sm.load()

    """# removing verbs
    for name in names:
        doc = nlp(name)
        for ent in doc.ents:
            if ent.label_ == 'VERB':
                names.remove(name)
    """

    # removing 's
    for name in names:
        if name[-2:] == "'s":
            names[names.index(name)] = name.replace("'s", "")

    """for name in names:
        first_last = HumanName(name).first + ' ' + HumanName(name).last
        print(first_last)
        filtered_people.append(name)
    return filtered_people"""
    return names


def print_character_names(book_address):
    """
    prints all characters' name and last name found in the book
    """
    book_read = open(book_address, "r")
    # whole book as a string
    book_lines = book_read.readlines()
    text = ""
    for i in range(len(book_lines)):
        text = text + book_lines[i]

    names = get_character_names_v2(text)
    print("FIRST LAST")
    for name in names:
        first_last = HumanName(name).first + ' ' + HumanName(name).last
        print(first_last)


def create_character_graph(book_address):
    """
    :param book_address:
    :return graph: networkx graph, nodes are labeled 0, 1, ...
    :return names: list of node names, names[i] = name of node i in the graph.
    :return counts: number of each name's appearance in the text, name[i] is found count[i] times
    """
    book_read = open(book_address, "r")
    # whole book as a string
    text = ""
    names = []
    counts = []
    graph = nx.Graph()
    for li, line in enumerate(book_read.readlines()):
        text = text + line
        if li % 30 == 1:
            new_names = get_character_names_v3(text)
            for name in new_names:
                if name not in names:
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
            text = ""
    print(graph.edges())
    print(graph.nodes())
    return graph, names, counts


if __name__ == '__main__':
    create_character_graph(book_address="C:/Users/amin/OneDrive - York University/Courses/Data analysis and "
                                        "visualization/Projects/Gutenberg/txt/Charles Dickens___A Christmas Carol.txt")
