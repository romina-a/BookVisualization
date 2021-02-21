from nltk.tag import StanfordNERTagger
from nltk import word_tokenize
import os

from nltk.parse import CoreNLPParser

# Note: This is to check how StanfordNER works

# ~~~~~~~~~~~~~~~~~~method 1, deprecated~~~~~~~~~~~~~~~~~~~
# Path to stanford-ner folder
PATH = "./stanford-ner-2020-11-17"
CLASSIFIER_PATH = os.path.join(PATH, "classifiers/english.all.3class.distsim.crf.ser.gz")
JAR_PATH = os.path.join(PATH, "stanford-ner.jar")
st = StanfordNERTagger(CLASSIFIER_PATH, JAR_PATH)

# ~~~~~~~~~~~~~~~~~~method 2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

S = "Romina Abadi says hello to Amin."
print(S)
print("\t", st.tag(word_tokenize(S)))

S = "Sarah Anderson says hello to Jack."
print(S)
print("\t", st.tag(word_tokenize(S)))

S = "Sarah Anderson says hello to her friend Jack."
print(S)
print("\t", st.tag(word_tokenize(S)))

S = "Sarah, Mike, and their friend, Tom, are going to see Sarah's sister Addy."
print(S)
print("\t", st.tag(word_tokenize(S)))

S = "I am Romina Abadi. Hello Amin."
print(S)
print("\t", st.tag(word_tokenize(S)))

S = "Sarah Anderson, Mike Pence, and their friend," \
    " Tom Gholizadeh, are going to see Sarah's sister, Addy." \
    " Sarah and Addy work at Mrs. Spencer's coffee shop: Amadeus Patisserie."
