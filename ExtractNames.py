import nltk
import os
import stanza
from nltk.parse import CoreNLPParser
import spacy
from nltk.tag import StanfordNERTagger


# ~~~~~~~~~~~~~~~~~~~~~~~~~Name Extraction Methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


# TODO force include prefixes
# TODO use filtering
def get_character_names_stanford_server(text):  # using stanford
    """
    MUST have the Stanford CoreNLP server running
    NOTE source: https://github.com/nltk/nltk/wiki/Stanford-CoreNLP-API-in-NLTK

    :param text: raw text
    :return: list of strings, all the names (repetitions are not removed)
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
