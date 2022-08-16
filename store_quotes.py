import sqlite3
import json
import uuid

def enable_foreign_keys():        ## to enable foreign keys
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    connection.commit()

def create_author_table():         ## to create author table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS author")
    cursor.execute("""CREATE TABLE author
    (
        id INT NOT NULL PRIMARY KEY,
        author_name VARCHAR(200),
        author_born_details TEXT
    );""")
    connection.commit()

def create_quote_table():          ## to create quote table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS quote")
    cursor.execute("""CREATE TABLE quote
    (
        id INT NOT NULL PRIMARY KEY,
        quote TEXT,
        author_id INT,
        FOREIGN KEY(author_id) REFERENCES author(id) ON DELETE CASCADE
    );""")
    connection.commit()

def create_tag_table():             ## to create tag table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS tag")
    cursor.execute("""CREATE TABLE tag
    (
        id INT NOT NULL PRIMARY KEY,
        tag_name VARCHAR(200)
    );
    """)
    connection.commit()

def create_quote_tags_table():          ## to create quote tags table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS quote_tags")
    cursor.execute("""CREATE TABLE quote_tags
    (
        id INT NOT NULL PRIMARY KEY,
        tag_id INT,
        quote_id INT,
        FOREIGN KEY(tag_id) REFERENCES tag(id) ON DELETE CASCADE,
        FOREIGN KEY(quote_id) REFERENCES quote(id) ON DELETE CASCADE
    );""")
    connection.commit()

def get_json_data():                 ## to get data from json object
    json_data = json.load(open('quotes.json'))
    quotes = json_data["quotes"]
    authors = json_data["authors"]
    return quotes,authors

def insert_values_into_author_table(authors):         ## insert values into author table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    for i in range(len(authors)):
        required_author_details = authors[i]
        tuple_of_values = (i+1,required_author_details["name"],required_author_details["born"])
        cursor.execute(""" INSERT INTO author(id,author_name,author_born_details) VALUES (?,?,?)""", tuple_of_values)
        connection.commit()

def get_forien_key_value_of_author_id(author_name):      ## to get author id foreign key 
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    statement = "SELECT id from author WHERE author_name = ?"
    cursor.execute(statement,(author_name,))
    author_id, = cursor.fetchone()
    return author_id

def get_values_to_insert_into_quote_table(i,required_quote):   ## to get values to insert into quote table
    id = i+1
    quote = required_quote["quote"]
    author_name = required_quote["author"]
    author_id = get_forien_key_value_of_author_id(author_name)
    tuple_of_values = (id,quote,author_id)
    return tuple_of_values

def insert_values_into_quote_table(quotes):        ## insert values in to quote table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    for i in range(len(quotes)):
        required_quote = quotes[i]
        tuple_of_values = get_values_to_insert_into_quote_table(i,required_quote)
        cursor.execute(""" INSERT INTO quote(id,quote,author_id) VALUES (?,?,?)""", tuple_of_values)
        connection.commit()

def get_unique_tags_list(quotes):        ## to get unique tags list
    unique_tags_list = []
    for quote in quotes:
        tags_list = quote['tags']
        for tag in tags_list:
            if tag not in unique_tags_list:
                unique_tags_list.append(tag)
    return unique_tags_list

def insert_values_into_tag_table(unique_tags_list):      ## insert values into tag table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    id = 1
    for tag in unique_tags_list:
        tuple_of_values = (id,tag)
        id += 1 
        cursor.execute(""" INSERT INTO tag(id,tag_name) VALUES (?,?)""", tuple_of_values)
        connection.commit()

def get_tag_id_of_a_tag(tag):       ## to get tag id foreign key
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    cursor.execute(""" SELECT id FROM tag WHERE tag_name = ?""",(tag,))
    tag_id, = cursor.fetchone()
    return tag_id

def insert_values_into_quote_tags_table(quote_id,tags_list_of_quote):     ## insert values into quote tags table
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    for tag in tags_list_of_quote:
        id = str(uuid.uuid4())
        tag_id = get_tag_id_of_a_tag(tag)
        cursor.execute(""" INSERT INTO quote_tags(id,tag_id,quote_id) VALUES (?,?,?)""", (id,tag_id,quote_id))
        connection.commit()

def get_and_insert_list_of_tags_of_each_quote(quotes):
    for i in range(len(quotes)):
        required_quote = quotes[i]
        quote_id = i+1
        tags_list_of_quote = required_quote["tags"]
        insert_values_into_quote_tags_table(quote_id,tags_list_of_quote)

def calling_all_functions():
    quotes,authors = get_json_data()
    create_author_table()
    create_quote_table()
    create_tag_table()
    create_quote_tags_table()
    enable_foreign_keys()
    insert_values_into_author_table(authors)
    insert_values_into_quote_table(quotes)
    unique_tags_list = get_unique_tags_list(quotes)
    insert_values_into_tag_table(unique_tags_list)
    get_and_insert_list_of_tags_of_each_quote(quotes)
    
calling_all_functions()

