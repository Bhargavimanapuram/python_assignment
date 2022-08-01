import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import json

def get_quote_text(each_quote):    ## to get quote text for each quote for all pages
    quote_element = each_quote.find('span',attrs={'class':'text'})
    quote= quote_element.getText()
    quote_a = quote.strip(' " ')
    return quote_a

def get_author_of_quote(each_quote):   ## to get author name of each quote for all pages
    author_element = each_quote.find("small",attrs={'class':'author'})
    author=author_element.getText()
    return author

def get_tags_list(each_quote):     ## to get tags list for each quote for all pages
    tags_container = each_quote.find('div',attrs={'class':'tags'})
    list_of_tag_ele = tags_container.find_all('a',attrs={'class':'tag'})
    list_of_tags = []
    for ele in list_of_tag_ele:
        list_of_tags.append(ele.getText())
    return list_of_tags
        
        
def get_list_of_quotes(data):     ## to get list of all quotes for a page
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

def get_author_details(author_data,author_url):   ## to get author details in about author page
    soup = BeautifulSoup(author_data, 'html.parser')
    author_page_content = soup.find('div',attrs={'class':'author-details'})
    author_name_element = author_page_content.find('h3',attrs={'class':'author-title'})
    author_name = author_name_element.getText()
    born_details_elements = author_page_content.find_all('span')
    born_details = born_details_elements[0].getText() +" "+ born_details_elements[1].getText()
    author_details={
        'name':author_name,
        'born':born_details,
        'reference':author_url
    }
    return(author_details)


def get_list_of_authors(data):    ## to get list of all auther details for a page
    soup = BeautifulSoup(data, 'html.parser')
    list_of_all_authors_containers = soup.find_all('div', attrs={'class': 'quote'})
    list_of_sub_authors = []
    for each_quote in list_of_all_authors_containers:
        quote_elements = each_quote.find_all('a')
        author_href = quote_elements[0].get('href')
        author_url = "http://quotes.toscrape.com" + author_href + "/"
        author_data = urllib.request.urlopen(author_url)
        author_details = get_author_details(author_data,author_url)
        list_of_sub_authors.append(author_details)
    return list_of_sub_authors


page = 1
list_of_quotes = []
list_of_authors = []
while page <= 10:       ## iterating over each page 
    try:
        url = "http://quotes.toscrape.com/page/" + str(page) + "/"

        data = urllib.request.urlopen(url)
        list_of_sub_authors = get_list_of_authors(data)
        list_of_authors.extend(list_of_sub_authors)

        data = urllib.request.urlopen(url)
        list_of_sub_quotes = get_list_of_quotes(data)
        list_of_quotes.extend(list_of_sub_quotes)
        page += 1
    except:
        break

quotes_author_object = {
    'quotes' : list_of_quotes,
    'authors': list_of_authors
}

json_object = json.dumps(quotes_author_object)
print(list_of_quotes[0])