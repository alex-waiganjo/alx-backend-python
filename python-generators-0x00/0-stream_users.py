import mysql.connector

def stream_users():
    """
    A generator that connects to the specified MySQL database, executes the given query,
    and yields rows one by one.
    """
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    conn.close()