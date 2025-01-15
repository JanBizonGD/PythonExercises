#!/usr/bin/python3

import uuid
import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()

# executemany
cur.execute("INSERT INTO login (loginText, passwordText, administrator, bearerToken) VALUES (?, ?, ?, ?)",
            ('admin', 'admin', 'TRUE', str(uuid.uuid4()))
            )
cur.execute("INSERT INTO pizza (nameText, ingredients, price) VALUES (?, ?, ?)",
            ("Margaritta", "[sos pomidorowy, cheese]", 20))
cur.execute("INSERT INTO pizza (nameText, ingredients, price) VALUES (?, ?, ?)",
            ("Capricciosa", "[sos pomidorowy, mozzarella, szynka, pieczarki]", 25))
cur.execute("INSERT INTO pizza (nameText, ingredients, price) VALUES (?, ?, ?)",
            ("Pepperoni", "[sos pomidorowy, mozzarella, pepperoni]", 27))
cur.execute("INSERT INTO pizza (nameText, ingredients, price) VALUES (?, ?, ?)",
            ("Hawaiian", "[sos pomidorowy, mozzarella, szynka, ananas]", 25))
cur.execute("INSERT INTO pizza (nameText, ingredients, price) VALUES (?, ?, ?)",
            ("Vegetariana", "[sos pomidorowy, mozzarella, papryka, pieczarki, cebula, oliwki, kukurydza]", 35))
cur.execute("INSERT INTO pizza (nameText, ingredients, price) VALUES (?, ?, ?)",
            ("Carbonara", "[sos smietanowy, mozzarella, boczek, jajko, parmezan]", 30))


connection.commit()
connection.close()
