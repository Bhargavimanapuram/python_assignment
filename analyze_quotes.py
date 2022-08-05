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
        select_query = "SELECT COUNT(id) AS total_no_of_quotations FROM quote;"
        cursor.execute(select_query)
        no_of_quotations, = cursor.fetchone()
        return no_of_quotations
    except sqlite3.Error as error:
        print(error)

def get_no_of_quotations_by_author(connection_obj,author_name):
    try:
        cursor = connection_obj.cursor()
        select_query = "SELECT COUNT(id) AS no_of_quotations FROM quote WHERE author_name = ?;"
        cursor.execute(select_query, (author_name,))
        no_of_quotations_by_author,= cursor.fetchone()
        cursor.close()
        return no_of_quotations_by_author
    except sqlite3.Error as error:
        print(error)

def create_view(connection_obj):
    try:
        cursor = connection_obj.cursor()
        view_query = "CREATE VIEW no_of_tags_per_quote AS SELECT COUNT(*) AS no_of_tags,quote_id FROM quote_tags GROUP BY quote_id"
        cursor.execute(view_query)
        cursor.close()
    except sqlite3.Error as error:
        print(error)


def get_minimum_maximum_average_no_of_tags(connection_obj):
    try:
        cursor = connection_obj.cursor()
        select_query = "SELECT MAX(no_of_tags) AS maximum_no_of_tags, MIN(no_of_tags) As minimum_no_of_tags ,AVG(no_of_tags) AS average_no_of_tags FROM no_of_tags_per_quote"
        cursor.execute(select_query)
        maximum,minimum,average = cursor.fetchone()
        cursor.close()
        return maximum,minimum,average
    except sqlite3.Error as error:
        print(error)


def get_top_n_authors(connection_obj,n):
    try:
        cursor = connection_obj.cursor()
        select_query = "SELECT author_name,count(id) AS no_of_quotations FROM quote GROUP BY author_id ORDER BY no_of_quotations DESC LIMIT ?;"
        cursor.execute(select_query, (n,))
        top_n_authors= cursor.fetchall()
        cursor.close()
        return top_n_authors
    except sqlite3.Error as error:
        print(error)

def calling_all_functions():
    connection_obj = get_sqlite_connection()
    no_of_quotations = get_total_no_of_quotations(connection_obj)
    no_of_quotations_by_author = get_no_of_quotations_by_author(connection_obj,"Albert Einstein")
    create_view(connection_obj)
    min_max_avg_of_tags = get_minimum_maximum_average_no_of_tags(connection_obj)
    top_n_authors = get_top_n_authors(connection_obj,5)
  
calling_all_functions()