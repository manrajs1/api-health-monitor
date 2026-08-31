from url_monitoring import request_check
from database_operations import add_monitor, save_check, get_check_history, get_monitors, delete_monitor, get_monitor

url = "https://example.com"

monitor = add_monitor(url)

result = request_check(url)
save_check(monitor["id"], result)

history = get_check_history(monitor['id'])
print(history)


print(get_monitors())

print(get_monitor(monitor['id']))
