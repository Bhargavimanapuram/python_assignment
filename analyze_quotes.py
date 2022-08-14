import sqlite3

def get_total_no_of_quotations():          ## to get total number of quotations on website
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    select_query = "SELECT COUNT(id) AS total_no_of_quotations FROM quote;"
    cursor.execute(select_query)
    no_of_quotations, = cursor.fetchone()
    connection.close()
    return no_of_quotations

def get_no_of_quotations_by_author(author_name):     ## to get total number of quotations by given author
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    select_query = """SELECT 
        author.author_name AS author_name, 
        COUNT(quote.id) AS no_of_quotations 
        FROM quote INNER JOIN author ON quote.author_id = author.id
        WHERE author.author_name = ?;"""
    cursor.execute(select_query, (author_name,))
    no_of_quotations_by_author = cursor.fetchone()
    connection.close()
    return no_of_quotations_by_author

def create_view():         ## to create view number of tags per quote
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    cursor.execute("DROP VIEW IF EXISTS no_of_tags_per_quote")
    view_query = """CREATE VIEW no_of_tags_per_quote AS 
        SELECT quote_id, COUNT(tag_id) AS no_of_tags 
        FROM quote_tags 
        GROUP BY quote_id"""
    cursor.execute(view_query)
    connection.close()

def get_minimum_maximum_average_no_of_tags():       ## to get minimum maximum average number of tags
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    select_query = """SELECT 
        MIN(no_of_tags) As minimum_no_of_tags,
        MAX(no_of_tags) AS maximum_no_of_tags,
        AVG(no_of_tags) AS average_no_of_tags 
        FROM no_of_tags_per_quote"""
    cursor.execute(select_query)
    min_max_avg_of_tags = cursor.fetchone()
    connection.close()
    return min_max_avg_of_tags

def get_top_n_authors(n):        ## to get top n authors who authored the maximum number of quotations 
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()
    select_query = """SELECT 
        quote.author_id AS author_id,
        author.author_name AS author_name,
        count(quote.id) AS no_of_quotations 
        FROM quote INNER JOIN author ON quote.author_id = author.id
        GROUP BY author_id 
        ORDER BY no_of_quotations DESC 
        LIMIT ?;"""
    cursor.execute(select_query, (n,))
    top_n_authors= cursor.fetchall()
    connection.close()
    return top_n_authors

def calling_all_functions():
    no_of_quotations = get_total_no_of_quotations()
    no_of_quotations_by_author = get_no_of_quotations_by_author("J.K. Rowling")
    create_view()
    min_max_avg_of_tags = get_minimum_maximum_average_no_of_tags()
    top_n_authors = get_top_n_authors(7)
    print(no_of_quotations)
    print(no_of_quotations_by_author)
    print(min_max_avg_of_tags)
    print(top_n_authors)

calling_all_functions()
