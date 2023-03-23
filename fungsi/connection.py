import sqlite3

def connection():
    # conn = sqlite3.connect('database/dbtweet.db')
    conn = sqlite3.connect('database/dbtweet.db')
    # cursor = conn.cursor()
    return conn

    
