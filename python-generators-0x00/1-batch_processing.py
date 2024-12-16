#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size: int):
    """
    A generator that connects to the specified MySQL database, executes the given query,
    and yields rows in batches.
    """
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    conn.close()
    

def batch_processing(batch_size: int):
    """
    Process the rows in batches.
    """
    
    for batch in stream_users_in_batches(batch_size):
        for row in batch:
            if row[3] > 25:
                print({'user_id': row[0], 'name': row[1], 'email': row[2], 'age': row[3]}, end="\n\n")
        return None