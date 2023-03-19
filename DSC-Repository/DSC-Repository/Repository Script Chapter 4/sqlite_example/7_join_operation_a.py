import sqlite3

conn = sqlite3.connect('data/binar_data_science_join.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE users (username varchar(255), email varchar(255));''')
print("Table 'users' created successfully")

conn.execute("INSERT INTO users (username, email) VALUES ('binaria', 'binaria@binar.com')")
conn.execute("INSERT INTO users VALUES ('bintang', 'bintang@binar.com')")
print("Insert to Table 'users' is successfully")

conn.execute('''CREATE TABLE hobbies (name varchar(255), user_id INT, FOREIGN KEY (user_id) REFERENCES users(rowid));''')
print("Table 'hobbies' created successfully")

conn.execute("INSERT INTO hobbies (name, user_id) VALUES ('football', 1);")
conn.execute("INSERT INTO hobbies (name, user_id) VALUES ('gaming', 2);")
conn.execute("INSERT INTO hobbies (name, user_id) VALUES ('traveling', 2);")
print("Insert to Table 'hobbies' is successfully")

conn.commit()
print("Records created successfully")
conn.close()