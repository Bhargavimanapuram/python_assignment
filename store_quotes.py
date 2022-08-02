import sqlite3
import json

connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS quote")

cursor.execute("""CREATE TABLE quote
(
    id INT NOT NULL PRIMARY KEY,
    quote TEXT,
    author_name VARCHAR(200),
    no_of_tags INT
);""")

print("Table quote is ready")

cursor.execute("DROP TABLE IF EXISTS author_details")

cursor.execute("""CREATE TABLE author_details
(
    id INT NOT NULL PRIMARY KEY,
    author_name TEXT,
    author_born_details VARCHAR(200)
);""")

print("table author_details is ready")

json_data = json.load(open('quotes.json'))

quotes = json_data["quotes"]
authors = json_data["authors"]

for i in range(len(quotes)):
    required_quote = quotes[i]
    tuple_of_values = (i+1,required_quote["quote"],required_quote["author"],len(required_quote["tags"]))
    cursor.execute(""" INSERT INTO quote(id,quote,author_name,no_of_tags) VALUES (?,?,?,?)""", tuple_of_values)

print("Data Inserted in the table: ")

for i in range(len(authors)):
    required_author_details = authors[i]
    tuple_of_values = (i,required_author_details["name"],required_author_details["born"])
    cursor.execute(""" INSERT INTO author_details(id,author_name,author_born_details) VALUES (?,?,?)""", tuple_of_values)

print("Data Inserted in the table: ")
