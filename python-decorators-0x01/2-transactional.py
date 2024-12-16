import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('users.db')
        kwargs['connection'] = connection
        try:
            return func(*args, **kwargs)
        finally:
            connection.close()
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = kwargs.get('connection')
        if connection is None:
            raise ValueError("No DB connection found")
        connection.execute('BEGIN')
        try:
            result = func(*args, **kwargs)
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(connection, user_id, new_email):
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Test de mise à jour
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("User email updated successfully!")