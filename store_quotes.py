import sqlite3
import json
import uuid

def get_sqlite_connection():
    try:
        connection = sqlite3.connect('quotes.db')
        cursor = connection.cursor()
        return cursor,connection
    except sqlite3.Error as error:
        print(error)

def enable_foreign_keys(connection,cursor):
    cursor.execute("PRAGMA foreign_keys = ON")
    connection.commit()

def create_author_table(connection,cursor):
    cursor.execute("DROP TABLE IF EXISTS author")
    cursor.execute("""CREATE TABLE author
    (
        id INT NOT NULL PRIMARY KEY,
        author_name VARCHAR(200),
        author_born_details TEXT
    );""")
    connection.commit()

def create_quote_table(connection,cursor):
    cursor.execute("DROP TABLE IF EXISTS quote")
    cursor.execute("""CREATE TABLE quote
    (
        id INT NOT NULL PRIMARY KEY,
        quote TEXT,
        author_name VARCHAR(200),
        author_id INT,
        FOREIGN KEY(author_id) REFERENCES author(id) ON DELETE CASCADE
    );""")
    connection.commit()

def create_quote_tags_table(connection,cursor):
    cursor.execute("DROP TABLE IF EXISTS quote_tags")
    cursor.execute("""CREATE TABLE quote_tags
    (
        id VARCHAR(200) NOT NULL PRIMARY KEY,
        tag_name VARCHAR(200),
        quote_id INT,
        author_id INT,
        FOREIGN KEY(quote_id) REFERENCES quote(id) ON DELETE CASCADE,
        FOREIGN KEY(author_id) REFERENCES author(id) ON DELETE CASCADE
    );""")
    connection.commit()

def get_json_data():
    json_data = json.load(open('quotes.json'))
    quotes = json_data["quotes"]
    authors = json_data["authors"]
    return quotes,authors

def insert_values_into_author_table(authors,connection,cursor):
    for i in range(len(authors)):
        required_author_details = authors[i]
        tuple_of_values = (i+1,required_author_details["name"],required_author_details["born"])
        cursor.execute(""" INSERT INTO author(id,author_name,author_born_details) VALUES (?,?,?)""", tuple_of_values)
        connection.commit()

def get_forien_key_value_of_author_id(author_name,cursor):
    statement = "SELECT id from author WHERE author_name = ?"
    data = cursor.execute(statement,(author_name,))
    for row in data:
        author_id, = row
        return author_id

def insert_values_into_quote_table(quotes,connection,cursor):
    for i in range(len(quotes)):
        required_quote = quotes[i]
        id = i+1
        quote = required_quote["quote"]
        author_name = required_quote["author"]
        author_id = get_forien_key_value_of_author_id(author_name,cursor)
        tuple_of_values = (id,quote,author_name,author_id)
        cursor.execute(""" INSERT INTO quote(id,quote,author_name,author_id) VALUES (?,?,?,?)""", tuple_of_values)
        connection.commit()

def get_forien_key_values_for_quote_tags_table(quote_id,cursor):
    statement = "SELECT author_id from quote WHERE id = ?"
    data = cursor.execute(statement,(quote_id,))
    for row in data:
        author_id, = row
        return author_id

def insert_values_into_quote_tags_table(quote_id,tags_list_of_quote,author_id,connection,cursor):
    for tag in tags_list_of_quote:
        tag_id = str(uuid.uuid4())
        tag_name = tag
        tuple_of_values = (tag_id,tag_name,quote_id,author_id)
        cursor.execute(""" INSERT INTO quote_tags(id,tag_name,quote_id,author_id) VALUES (?,?,?,?)""", tuple_of_values)
        connection.commit()

def get_and_insert_list_of_tags_of_each_quote(quotes,connection,cursor):
    for i in range(len(quotes)):
        required_quote = quotes[i]
        quote_id = i+1
        tags_list_of_quote = required_quote["tags"]
        author_id = get_forien_key_values_for_quote_tags_table(quote_id,cursor)
        insert_values_into_quote_tags_table(quote_id,tags_list_of_quote,author_id,connection,cursor)
        
#def get_data(cursor):
    #data=cursor.execute('''SELECT * FROM author''')
    #for row in data:
        #print(row)


def calling_all_functions():
    quotes,authors = get_json_data()
    cursor,connection = get_sqlite_connection()
    create_author_table(connection,cursor)
    create_quote_table(connection,cursor)
    create_quote_tags_table(connection,cursor)
    enable_foreign_keys(connection,cursor)
    insert_values_into_author_table(authors,connection,cursor)
    insert_values_into_quote_table(quotes,connection,cursor)
    get_and_insert_list_of_tags_of_each_quote(quotes,connection,cursor)

calling_all_functions()
