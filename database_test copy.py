import sqlite3
import datetime
from url_request_check import request_check
from database import add_monitor

connection = sqlite3.connect("monitor.db")
cur = connection.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
url = "https://example.com"
# Adding this url into our monitors table using placeholder
'''cur.execute("INSERT INTO monitors(url) VALUES (?)", (url,))
# Assigning the id from the latest monitor added and assigning it to the checks table monitor id for foreign key
monitor_id = cur.lastrowid

# Saving
connection.commit()
'''
add = add_monitor(url)
monitor_id = add["id"]
urlcheck = request_check(url)





#Printing all monitors created so far
res = cur.execute("SELECT id, url FROM monitors")
print(res.fetchall())

status_code = 200
response_time = 0.42
time = datetime.datetime.now(datetime.timezone.utc )
timestamp = str(time)
up = 1
error = None

# Inserting into checks table data with linked monitor_id
cur.execute("""
INSERT INTO checks(monitor_id, status_code, response_time, 
    timestamp, up, error)
    VALUES(?,?,?,?,?,?)""",
    (monitor_id, status_code, response_time, timestamp, up, error)
)
connection.commit()
res = cur.execute("SELECT * FROM checks")
print(res.fetchall())


connection.close()