import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import pandas as pd

def basic_clean(string):
    # lowercase everything
    string = string.lower()
    
    # Normalize unicode characters
    string = unicodedata.normalize('NFKD', string)\
        .encode('ascii', 'ignore')\
        .decode('utf-8', 'ignore')
    
    # remove anything that is not a through z, a number, a single quote, or whitespace
    return re.sub(r"[^a-z0-9'\s]", '', string)



def stem(string):
    """
    Stem the words in the input string using the Porter stemming algorithm.

    Args:
        string (str): The input string to be stemmed.

    Returns:
        str: The input string after applying stemming to each word.
    """
    # Create Porter stemmer
    ps = nltk.porter.PorterStemmer()

    # Stem each word in the string
    stems = [ps.stem(word) for word in string.split()]

    # Join the stemmed words back into a string
    stemmed = ' '.join(stems)

    return stemmed

def lemmatize(string):
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()

    #use lemmatize - apply stem to each word in our string
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    #join words back together
    lemma = ' '.join(lemmas)

    return lemma


def remove_stopwords(text, extra_words=None, exclude_words=None):
    # Get the default English stopwords list from NLTK
    stopwords_list = set(stopwords.words('english'))

    # Add extra words to the stopwords list
    if extra_words:
        stopwords_list.update(extra_words)

    # Remove exclude words from the stopwords list
    if exclude_words:
        stopwords_list.difference_update(set(exclude_words))

    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove stopwords from the list of words
    filtered_words = [word for word in words if word.lower() not in stopwords_list]

    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)

    return filtered_text
