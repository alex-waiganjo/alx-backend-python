import mysql.connector

# Db Connection class
class DatabaseConnection():
        
    def __init__(self, user, host, password, database):
        self.user = user
        self.host = host
        self.password = password
        self.database = database
    
    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=self.user,
            host=self.host,
            password=self.password,
            database=self.database
        )
        
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        if exc_type is not None:
            return False
        return True
    
# Entry Point
if __name__ == "__main__":
    with DatabaseConnection('root', 'localhost', '', 'ALX_prodev') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            print(row)