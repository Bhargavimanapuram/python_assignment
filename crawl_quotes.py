from bs4 import BeautifulSoup
import urllib.request
import json

def get_quote_text(each_quote):    ## to get quote text for each quote for all pages
    quote_element = each_quote.find('span',attrs={'class':'text'})
    quote_text= quote_element.get_text()
    quote= quote_text[1:-1]
    return quote

def get_author_of_quote(each_quote):   ## to get author name of each quote for all pages
    author_element = each_quote.find("small",attrs={'class':'author'})
    author=author_element.get_text()
    return author

def get_tags_list(each_quote):     ## to get tags list for each quote for all pages
    tags_container = each_quote.find('div',attrs={'class':'tags'})
    list_of_tag_elements= tags_container.find_all('a',attrs={'class':'tag'})
    list_of_tags = []
    for element in list_of_tag_elements:
        list_of_tags.append(element.getText())
    return list_of_tags
        
def get_quote_object(each_quote):    ## to get quote object for each quote
    quote_object = {
        'quote':get_quote_text(each_quote),
        'author':get_author_of_quote(each_quote),
        'tags':get_tags_list(each_quote)
    }
    return(quote_object)

def get_quotes_of_each_page(soup):        ## to get list of quotes for a page
    quotes_containers = soup.find_all('div', attrs={'class': 'quote'})
    list_of_quotes_for_a_page = []
    for each_quote in quotes_containers:
        quote_object = get_quote_object(each_quote)
        list_of_quotes_for_a_page.append(quote_object)
    return list_of_quotes_for_a_page

def get_author_link_and_name(each_quote):      ## get author link and name for each quote
    quote_anchor_elements = each_quote.find_all('a')
    author_link = quote_anchor_elements[0].get('href')
    author_name = get_author_of_quote(each_quote)
    author_link_object = {"author_link":author_link,"author_name":author_name}
    return author_link_object

def get_author_urls_of_page(soup):       ## get list of author links for a page
    quotes_containers = soup.find_all('div', attrs={'class': 'quote'})
    unique_author_links_for_page = []
    for each_quote in quotes_containers:
        author_link_object = get_author_link_and_name(each_quote)
        if author_link_object not in unique_author_links_for_page:
            unique_author_links_for_page.append(author_link_object)
    return unique_author_links_for_page

def appending_author_links(author_links,unique_author_links_for_page):   ## appending unique author link
    updated_author_links = []
    updated_author_links.extend(author_links)
    for link in unique_author_links_for_page:
        if link not in updated_author_links:
            updated_author_links.append(link)
    return updated_author_links
    
def get_born_details_of_author(author_link_item):        ## get born details of an author
    url = "http://quotes.toscrape.com" + author_link_item['author_link'] + "/"
    data = urllib.request.urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')
    author_page_content = soup.find('div',attrs={'class':'author-details'})
    born_details_elements = author_page_content.find_all('span')
    born_details = born_details_elements[0].getText() +" "+ born_details_elements[1].getText()
    return born_details

def get_author_object(author_link_item,born_details):   ## to get author object
    author_object={
            'name':author_link_item['author_name'],
            'born':born_details,
            'reference':"http://quotes.toscrape.com" + author_link_item['author_link'] + "/"
        }
    return author_object

def get_author_details(author_links):   ## to get author details in about author page
    list_of_authors = []
    for author_link_item in author_links:
        born_details = get_born_details_of_author(author_link_item)
        author_object = get_author_object(author_link_item,born_details)
        list_of_authors.append(author_object)
    return list_of_authors

def access_quote_author_page(url):   ## get list of quotes for a page 
    data = urllib.request.urlopen(url)
    soup = BeautifulSoup(data,'html.parser')
    list_of_quotes_for_a_page = get_quotes_of_each_page(soup)
    unique_author_links_for_page = get_author_urls_of_page(soup)
    return list_of_quotes_for_a_page,unique_author_links_for_page

def get_url_of_page(url):          ## to get url of each page
    data = urllib.request.urlopen(url)
    soup = BeautifulSoup(data,'html.parser')
    page_url_element = (soup.find("li",attrs={"class":"next"})).find('a')
    page_url = page_url_element.get('href')
    return page_url   

def accessing_each_page_details():         ## iterating on each page
    list_of_quotes = []
    author_links = []
    url = "http://quotes.toscrape.com/"
    while True:
        try:
            list_of_quotes_for_a_page,unique_author_links_for_page= access_quote_author_page(url)
            list_of_quotes.extend(list_of_quotes_for_a_page)
            updated_author_links = appending_author_links(author_links,unique_author_links_for_page)
            author_links = updated_author_links
            page_url = get_url_of_page(url)
            url = "http://quotes.toscrape.com" + page_url
        except:
            break
    return list_of_quotes,author_links

def get_quotes_author_object(list_of_quotes,list_of_authors):   ## to get quotes authors object
    quotes_author_object = {
    'quotes' : list_of_quotes,
    'authors': list_of_authors
    }
    return quotes_author_object
    
def object_saved_in_json_file(quotes_author_object):        ## json object written in json file
    json_object = json.dumps(quotes_author_object,ensure_ascii=False)
    file = open('quotes.json','w')
    file.write(json_object)
    file.close()

def calling_all_functions():
    list_of_quotes,author_links = accessing_each_page_details()
    list_of_authors = get_author_details(author_links)
    quotes_author_object = get_quotes_author_object(list_of_quotes,list_of_authors)
    object_saved_in_json_file(quotes_author_object)
    
calling_all_functions()