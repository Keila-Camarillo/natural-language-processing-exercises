import requests
from requests import get 
from bs4 import BeautifulSoup
import pandas as pd

import time


def create_soup(url):
    headers = {"User-Agent": "Chrome/91.0.4472.124"}

    response = get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

def get_blog_articles(url='https://codeup.com/blog/'):
    # Make a soup variable holding the response content
    soup = create_soup(url)
    
    # list of links
    blog_links = [element["href"] for element in soup.find_all("a", class_="more-link")]

    article_dict = []
    for link in blog_links:
        # get access to pages
        soup = create_soup(link)
        # title
        title = soup.h1.text
        # content info
        
        # append dict to list
        content_dict = {"title": title, 
                        "content": soup.find('div', class_="entry-content").text}
        article_dict.append(content_dict)
    return article_dict

def get_news_articles(url="https://blog.inshorts.com/"):
    pages = [f"{url}page/{i}/" for i in range(2,7)]
    for p in pages:
        soup = create_soup(p)
    
  
        # list of links from website
        links_list = [i.find("a")["href"] for i in soup.find_all("h2", class_="entry-title")]
        category_list = [i["class"][7] for i in soup.find_all("article")]
        article_dict = []
        for link in links_list:
            # get access to pages
            soup = create_soup(link)
            # title
            title = soup.h1.text
            # content info
            text_list = [p.get_text(strip=True) for div in soup.find_all("div", class_="entry-content") for p in div.find_all("p")]
            # list of category names
            category_list = [i["class"][6][9:] for i in soup.find_all("article")]
            # append dict to list

            content_dict = {"title": title, "content": text_list, "category": category_list}
            article_dict.append(content_dict)
    return article_dict
