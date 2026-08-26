import sqlite3
import datetime
from url_request_check import request_check

connection = sqlite3.connect("monitor.db")
cur = connection.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
url = "https://example.com"
# Adding this url into our monitors table using placeholder
cur.execute("INSERT INTO monitors(url) VALUES (?)", (url,))
# Assigning the id from the latest monitor added and assigning it to the checks table monitor id for foreign key
monitor_id = cur.lastrowid

# Saving
connection.commit()

#Printing all monitors created so far
res = cur.execute("SELECT id, url FROM monitors")
print(res.fetchall())

check_result = request_check(url)
status_code = check_result["status code"]
response_time = check_result["response time"]
time = datetime.datetime.now(datetime.timezone.utc )
timestamp = str(time)
up = check_result["Up"]
error = check_result["Error"]

# Inserting into checks table data with linked monitor_id
cur.execute("""
INSERT INTO checks(monitor_id, status_code, response_time, 
    timestamp, up, error)
    VALUES(?,?,?,?,?,?)""",
    (monitor_id, status_code, response_time, timestamp, up, error)
)
connection.commit()
res = cur.execute("SELECT * FROM checks WHERE monitor_id = ? ", (monitor_id,))
print(res.fetchall())


connection.close()