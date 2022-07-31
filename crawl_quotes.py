import requests
from bs4 import BeautifulSoup
import urllib.request
import re

def get_quote_text(each_quote):
    quote_element = each_quote.find('span',attrs={'class':'text'})
    quote=quote_element.getText()
    return quote

def get_author_of_quote(each_quote):
    author_element = each_quote.find("small",attrs={'class':'author'})
    author=author_element.getText()
    return author

def get_tags_list(each_quote):
    tags_container = each_quote.find('div',attrs={'class':'tags'})
    list_of_tag_ele = tags_container.find_all('a',attrs={'class':'tag'})
    list_of_tags = []
    for ele in list_of_tag_ele:
        list_of_tags.append(ele.getText())
    return list_of_tags
        
        
def get_list_of_quotes(data):
    soup = BeautifulSoup(data, 'html.parser')
    list_of_all_quotes_containers = soup.find_all('div', attrs={'class': 'quote'})
    list_of_sub_quotes = []
    for each_quote in list_of_all_quotes_containers:
        quote_dict = {
            'quote':get_quote_text(each_quote),
            'author':get_author_of_quote(each_quote),
            'tags_list':get_tags_list(each_quote)
        }
        list_of_quotes.append(quote_dict)
    return list_of_sub_quotes

page = 1
list_of_quotes = []
while page <= 10:
    try:
        url = "http://quotes.toscrape.com/page/" + str(page) + "/"
        data = urllib.request.urlopen(url)
        list_of_sub_quotes = get_list_of_quotes(data)
        list_of_quotes.extend(list_of_sub_quotes)
        page += 1
    except:
        break


