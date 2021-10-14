import re
import string
import Stemmer


STEMMER = Stemmer.Stemmer('english')

def tokenize(text):
    return text.split()

def lowercase_filter(tokens):
    return [token.lower() for token in tokens]

def stem_filter(tokens):
    return STEMMER.stemWords(tokens)

def analyze(text):
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = stem_filter(tokens)

    return [token for token in tokens if token]