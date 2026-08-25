import sqlite3

connection = sqlite3.connect("monitor.db")
cur = connection.cursor()

url = "https://example.com"
cur.execute("INSERT INTO monitors(url) VALUES (?)", (url,))
connection.commit()

res = cur.execute("SELECT id, url FROM monitors")
print(res.fetchall())

connection.close()