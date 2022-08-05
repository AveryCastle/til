import random
from urllib.request import Request, urlopen
import sys

WORD_URL = "http://learncodethehardway.org/words.txt"
WORDS = []

PHRASES = {
"class %%%(%%%):": "Make a class named %%% that is-a %%%.",
"class %%%(object):\n\tdef __init__(self, ***)" :"class %%% has-a __init__ that takes self and *** parameters.",
    "class %%%(object):\n\tdef ***(self, @@@)":
"class %%% has-a function named *** that takes self and @@@ parameters.", "*** = %%%()":
"Set *** to an instance of class %%%.", "***.***(@@@)":
"From *** get the *** function, and call it with parameters self, @@@.", "***.*** = '***'":
"From *** get the *** attribute and set it to '***'."
}

PHRASE_FIRST = False
if len(sys.argv) == 2 and sys.argv[1] == "english":
    PHRASE_FIRST = True


for word in urlopen(Request(WORD_URL)).readlines():
    WORDS.append(word.strip())

def convert(snippet, phrase):
    class_names = [w.capitalize() for w in random.sample(WORDS, snippet.count("%%%"))]
    other_names = random.sample(WORDS, snippet.count("***"))
    print(class_names)
    print(other_names)


try:
    while True:
        snippets = PHRASES.keys()
        random.shuffle(snippets)

    for snippet in snippets:
        phrase = PHRASES[snippet]
        question, answer = convert(snippet, phrase)
        if PHRASE_FIRST:
            question, answer = answer, question
            print(question)
        raw_input("> ")
        print("ANSWER: %s\n\n" % answer)

except EOFError:
    print("\nBye")
