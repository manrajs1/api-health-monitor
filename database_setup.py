import sqlite3

# Creating connection to the database
connection = sqlite3.connect("monitor.db")
# Creating messenger to send sql commands to the database
cur = connection.cursor()

# Creating a new table with id as primary key and url with required text value
cur.execute("CREATE TABLE IF NOT EXISTS monitors(id INTEGER PRIMARY KEY, url TEXT NOT NULL)")


# Closing the connection
connection.close()