import mysql.connector

class ExecuteQuery():
    def __init__(self, user, host, password, database, query, paramater) -> None:
        self.user=user
        self.host=host
        self.password=password
        self.password=password
        self.query=query
        self.database= database
        self.paramater=paramater
        
    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=self.user,
            host=self.host,
            password=self.password,
            database=self.database
        )
             
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, (self.paramater, ))
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        if exc_type is not None:
            return False
        return True
   
    
# Entry Point
if __name__ == "__main__":
    with ExecuteQuery('root', 'localhost', '', 'ALX_prodev', 'SELECT * FROM user_data where age > %s', 25) as rows:
        for row in rows:
            print(row)