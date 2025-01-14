import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()

cur.execute("INSERT INTO login (loginText, passwordText) VALUES (?, ?)",
            ('admin', 'admin')
            )

connection.commit()
connection.close()