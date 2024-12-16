import mysql.connector

seed = __import__('seed')

def paginate_users(page_size, offset):
    """
        Paginate the results of a query.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows
\
    
    
def lazy_paginate(page_size):
    """
    A generator function that uses paginate_users to lazily load pages.
    It yields one page at a time, fetching the next page only when needed.
    """
    offset = 0
    # Une seule boucle qui s'arrête lorsque plus aucune donnée n'est retournée
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size