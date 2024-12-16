#!/usr/bin/env python3
'''Objective: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset'''

import mysql.connector

config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'ALX_prodev'
    }
        
def stream_user_ages():
    '''stream user ages from the database'''
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    while True:
        row = cursor.fetchone()
        if not row:
            break
        yield row[0]
    cursor.close()
    connection.close()

def compute_ages():
    '''compute the average age of users in the database'''
    ages = stream_user_ages()
    total = 0
    count = 0
    for age in ages:
        total += age
        count += 1
    return total / count if count > 0 else 0

if __name__ == '__main__':
    print('Average age of users:', compute_ages())