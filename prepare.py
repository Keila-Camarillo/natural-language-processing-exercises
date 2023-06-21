import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

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