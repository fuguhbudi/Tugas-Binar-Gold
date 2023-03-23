import sqlite3

def connection():
    conn = sqlite3.connect('database/dbtweet.db')
    return conn

    
