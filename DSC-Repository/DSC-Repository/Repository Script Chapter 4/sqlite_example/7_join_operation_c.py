import sqlite3

conn = sqlite3.connect('data/binar_data_science_join.db')
print("Opened database successfully")
print()

print("List of Joined Data:")
cursor = conn.execute("SELECT users.username, hobbies.name \
            FROM users INNER JOIN hobbies ON users.rowid = hobbies.user_id")
for row in cursor:
    print(row)

print()
print("Operation done successfully")
conn.close()

