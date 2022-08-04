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
        
        
def get_author_details(author_data,author_url,author_name):   ## to get author details in about author page
    soup = BeautifulSoup(author_data, 'html.parser')
    author_page_content = soup.find('div',attrs={'class':'author-details'})
    born_details_elements = author_page_content.find_all('span')
    born_details = born_details_elements[0].getText() +" "+ born_details_elements[1].getText()
    author_details={
        'name':author_name,
        'born':born_details,
        'reference':author_url
    }
    return(author_details)


def appending_unique_list_of_authors(author_dict,list_of_authors_for_a_page): ## appending unique authors in authors list
    author_names_list = []
    updated_list_of_authors = []
    for author in list_of_authors_for_a_page:
        author_name = author['name']
        author_names_list.append(author_name)
    if author_dict['name'] not in author_names_list:
        updated_list_of_authors.extend(list_of_authors_for_a_page)
        updated_list_of_authors.append(author_dict)
        return updated_list_of_authors
    else:
        updated_list_of_authors.extend(list_of_authors_for_a_page)
        return updated_list_of_authors
        

def get_quote_and_author_deatils_of_each_page(soup):     ## to get list of all quote and author details for a page
    list_of_all_quotes_containers = soup.find_all('div', attrs={'class': 'quote'})
    list_of_quotes_for_a_page= []
    list_of_authors_for_a_page= []
    for each_quote in list_of_all_quotes_containers:
        quote_dict = {
            'quote':get_quote_text(each_quote),
            'author':get_author_of_quote(each_quote),
            'tags':get_tags_list(each_quote)
        }
        quote_anchor_elements = each_quote.find_all('a')
        author_href = quote_anchor_elements[0].get('href')
        author_url = "http://quotes.toscrape.com" + author_href + "/"
        author_data = urllib.request.urlopen(author_url)
        author_dict = get_author_details(author_data,author_url,quote_dict["author"])
        list_of_quotes_for_a_page.append(quote_dict)
        updated_list_of_authors = appending_unique_list_of_authors(author_dict,list_of_authors_for_a_page)
        list_of_authors_for_a_page= updated_list_of_authors
    return list_of_quotes_for_a_page,list_of_authors_for_a_page


list_of_quotes = []
list_of_authors = []
def get_list_of_all_authors_and_quotes(soup):  ## get list of all quotes and authors
    list_of_quotes_for_a_page,list_of_authors_for_a_page = get_quote_and_author_deatils_of_each_page(soup)
    list_of_quotes.extend(list_of_quotes_for_a_page)
    list_of_authors.extend(list_of_authors_for_a_page)

def accessing_each_page_details(): 
    page = 1
    while True:       ## iterating over each page 
        try:
            url = "http://quotes.toscrape.com/page/" + str(page) + "/"
            data = urllib.request.urlopen(url)
            soup = BeautifulSoup(data,'html.parser')
            content_containers = soup.find_all('div',attrs={'class':'col-md-8'})
            content_container_text = content_containers[1].getText()
            if "No quotes found!" not in content_container_text:
                get_list_of_all_authors_and_quotes(soup)
                page += 1
            else:
                break
        except:
            break


def get_quotes_author_object(list_of_quotes,list_of_authors):
    quotes_author_object = {
    'quotes' : list_of_quotes,
    'authors': list_of_authors
    }
    return quotes_author_object
    
def object_saved_in_json_file(quotes_author_object):
    json_object = json.dumps(quotes_author_object,ensure_ascii=False)
    file = open('quotes.json','w')
    file.write(json_object)
    file.close()

def calling_all_functions():
    accessing_each_page_details()
    quotes_author_object = get_quotes_author_object(list_of_quotes,list_of_authors)
    object_saved_in_json_file(quotes_author_object)

calling_all_functions()