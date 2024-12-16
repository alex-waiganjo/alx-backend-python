import csv
import mysql.connector


def connect_db() -> mysql.connector.connection.MySQLConnection:
    """
        Connect to a MySQL db
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="####",
    )


def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """
        Create a database.
    """
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")

    cursor.close()


def connect_to_prodev() -> None:
    """
        Connects to the ALX_prodev database.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="###",
        database="ALX_prodev"
    )

    return connection


def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """
        Creates the user_data table if it does not exist, with the required fields:
        user_id (UUID, PRIMARY KEY, Indexed)
        name (VARCHAR NOT NULL)
        email (VARCHAR NOT NULL)
        age (DECIMAL NOT NULL)
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) NOT NULL DEFAULT (UUID()),
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            PRIMARY KEY (user_id),
            INDEX (user_id)
        )
    """)
    cursor.close()


def insert_data(connection: mysql.connector.connection.MySQLConnection, data: str) -> None:
    """
        Insert data in csv file into the user_data table.
    """

    cursor = connection.cursor()

    try:
        with open(data, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Check if this user_id already exists
                cursor.execute(
                    "SELECT email FROM user_data WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result is None:
                    # Insert new record
                    cursor.execute(
                        "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)",
                        (name, email, age)
                    )
        connection.commit()
    except (FileNotFoundError, KeyError) as e:
        print(f"An error occurred while inserting data: {e}")
    finally:
        cursor.close()
