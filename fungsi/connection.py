import sqlite3

def connection():
    # conn = sqlite3.connect('database/dbtweet.db')
    connection = sqlite3.connect('database/dbtweet.db')
    cursor = connection.cursor()
    return cursor

    
