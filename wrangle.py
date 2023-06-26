#standard imports
import pandas as pd
import numpy as np

#parsing data
import re
import unicodedata
import nltk
from nltk.corpus import stopwords

import os
import json
import re

from requests import get
from bs4 import BeautifulSoup

def scrape_one_page(topic):
#topic = "business"
    base_url = "https://inshorts.com/en/read/"

    response = get(base_url + topic)

    soup = BeautifulSoup(response.content, 'html.parser')

    titles = soup.find_all('span', itemprop="headline")

    summaries = soup.find_all('div', itemprop="articleBody")

    summary_list = []

    for i in range(len(titles)):
        temp_dict = {"category": topic,
                    "title": titles[i].text,
                    "content": summaries[i].text}

        summary_list.append(temp_dict)

    return summary_list

def get_blog_articles(article_list):
    """
    
    """
    file = "blog_posts.json"
    
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
        
    
    headers = {'User-Agent': 'Codeup Data Science'}
    article_info = []

    for article in article_list:
        response = get(article, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        info_dict = {"title":soup.find("h1").text,
                    "link": article,
                    "date_published":soup.find('span', class_="published").text,
                    "content": soup.find('div', class_="entry-content").text}
        article_info.append(info_dict)
    
    with open(file, "w") as f:
        json.dump(article_info, f)
    return article_info

def get_news_articles(topic_list):
    """
    
    """
    file = "news_articles.json"
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)

    final_list = []

    for topic in topic_list:
        final_list.extend(scrape_one_page(topic))
    
    with open(file, "w") as f:
        json.dump(final_list, f)
        
    return final_list


def basic_clean(string):
    
    string = string.lower() #lowercasing
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8') #normalizing
    string = re.sub(r'[^a-z0-9\'\s]', '', string) #replace extra things
    
    return string

def tokenize(string):
    
    tokenize = nltk.tokenize.ToktokTokenizer() #creating the tokenize
    string = tokenize.tokenize(string, return_str=True) #using the tokenize
    
    return string


def stem(string):
    
    ps = nltk.porter.PorterStemmer() #creating my stemmer
    stems = [ps.stem(word) for word in string.split()] #splitting into each word and applying the stemmer
    string = ' '.join(stems) #joining all into one string
    
    return string

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    
    stopwords_ls = stopwords.words('english') #defining my stopwords
    
    stopwords_ls = set(stopwords_ls) - set(exclude_words) #removing any stopwords in my exclude list
    stopwords_ls = stopwords_ls.union(set(extra_words)) #adding any stopwards from my extra list
    
    words = string.split() #splitting up my string
    filtered_words = [word for word in words if word not in stopwords_ls] #use listcomp to remove words in stopwords_ls
    string = ' '.join(filtered_words) #joining back to a string
    
    return string

def lemmatize(string):
    
    wnl = nltk.stem.WordNetLemmatizer() #creating my lemmatizer
    lemmas = [wnl.lemmatize(word) for word in string.split()] #splitting my string into words and applying the lemma
    string = ' '.join(lemmas) #joining back into one string

    return string

def clean_df(df, extra_words=[], exclude_words=[]):
    """
    Send in df with columns: title and original,
    returns df with original, clean, stemmed, and lemmatized data
    """
    df['clean'] = df.original\
                        .apply(basic_clean)\
                        .apply(tokenize)\
                        .apply(remove_stopwords, 
                                    extra_words=extra_words,
                                    exclude_words=exclude_words)
    df['stemmed'] = df.clean.apply(stem)
    df['lemmatized'] = df.clean.apply(lemmatize)
    
    return df