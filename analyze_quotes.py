import sqlite3

def get_sqlite_connection():
    try:
        connection_obj = sqlite3.connect('quotes.db')
        return connection_obj

    except sqlite3.Error as error:
        print(error)

def get_total_no_of_quotations(connection_obj):
    try:
        cursor = connection_obj.cursor()
        select_query = "SELECT COUNT(id) FROM quote;"
        cursor.execute(select_query)
        no_of_quotations = cursor.fetchone()
        return no_of_quotations
    except sqlite3.Error as error:
        print(error)

def get_no_of_quotations_by_author(connection_obj,author_name):
    try:
        cursor = connection_obj.cursor()
        select_query = "SELECT COUNT(id) AS no_of_quotations FROM quote WHERE author_name = ?;"
        cursor.execute(select_query, (author_name,))
        no_of_quotations_by_author= cursor.fetchone()
        cursor.close()
        return no_of_quotations_by_author
    except sqlite3.Error as error:
        print(error)
            
def get_min_max_avg_of_tags(connection_obj):
    try:
        cursor = connection_obj.cursor()
        select_query = "SELECT max(no_of_tags), min(no_of_tags),avg(no_of_tags) FROM quote;"
        cursor.execute(select_query)
        min_max_avg_of_tags = cursor.fetchone()
        cursor.close()
        return min_max_avg_of_tags
    except sqlite3.Error as error:
        print(error)


def get_top_n_authors(connection_obj,n):
    try:
        cursor = connection_obj.cursor()
        select_query = "SELECT author_name,count(id) AS no_of_quotations FROM quote GROUP BY author_name ORDER BY no_of_quotations DESC LIMIT ?;"
        cursor.execute(select_query, (n,))
        top_n_authors= cursor.fetchall()
        cursor.close()
        return top_n_authors
    except sqlite3.Error as error:
        print(error)


connection_obj = get_sqlite_connection()
no_of_quotations = get_total_no_of_quotations(connection_obj)
no_of_quotations_by_author = get_no_of_quotations_by_author(connection_obj,"Albert Einstein")
min_max_avg_of_tags = get_min_max_avg_of_tags(connection_obj)
top_n_authors = get_top_n_authors(connection_obj,5)