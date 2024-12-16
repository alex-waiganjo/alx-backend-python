import time
import sqlite3 
import functools

#### paste your with_db_connection decorator here
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

""" your code goes here"""
def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Failed to execute {func.__name__}({args}, {kwargs}): {e}")
                    time.sleep(delay)
            raise Exception(f"Failed to execute {func.__name__} after {retries} retries")
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)