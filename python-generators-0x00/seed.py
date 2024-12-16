"""
Create the following functions
def connect_db() :- connects to the mysql database server
def create_database(connection):- creates the database ALX_prodev if it does not exist
def connect_to_prodev() connects the the ALX_prodev database in MYSQL
def create_table(connection):- creates a table user_data if it does not exists with the required fields
def insert_data(connection, data):- inserts data in the database if it does not exist
"""
import mysql.connector

def connect_db():
    try: 
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="####"
    ) 
        return connection
    except mysql.connector.Error:
        print("Database connection failed")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    yield connection

