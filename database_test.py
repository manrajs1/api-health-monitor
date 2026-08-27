import sqlite3
import datetime
from url_request_check import request_check
from database import add_monitor, save_check, get_check_history

url = "https://example.com"

monitor = add_monitor(url)

<<<<<<< HEAD
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
=======
result = request_check(url)
save_check(monitor["id"], result)

history = get_check_history(monitor['id'])
print(history)
>>>>>>> a53affe (add reusable database functions for monitors and check history)
