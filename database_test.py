import sqlite3
import datetime
from url_request_check import request_check
from database_operation import add_monitor, save_check, get_check_history, get_monitors, delete_monitor

url = "https://example.com"

monitor = add_monitor(url)

result = request_check(url)
save_check(monitor["id"], result)

history = get_check_history(monitor['id'])
print(history)


print(get_monitors())
delete_monitor(1)