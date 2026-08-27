import sqlite3
import datetime


def add_monitor(url):
    connection = sqlite3.connect("monitor.db")
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("INSERT INTO monitors(url) VALUES (?)", (url,))
    monitor_id = cur.lastrowid
    connection.commit()
    connection.close()
    return {"id" : monitor_id, "url":url}

def save_check(monitor_id, check_result):
    connection = sqlite3.connect("monitor.db")
    cur = connection.cursor()
    time = datetime.datetime.now(datetime.timezone.utc )
    timestamp = str(time)
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute('''
        INSERT INTO checks(monitor_id,
            status_code, 
            response_time, 
            timestamp, 
            up, 
            error) 
            VALUES (?,?,?,?,?,?)
    ''',    (monitor_id, check_result["status code"],
             check_result["response time"],
            timestamp, check_result["Up"],
            check_result['Error'])
    )
    connection.commit()
    connection.close()

def get_check_history(monitor_id):
    connection = sqlite3.connect("monitor.db")
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    rows = cur.execute('''
        SELECT * FROM checks WHERE monitor_id = ?
    ''', (monitor_id,))
    history = rows.fetchall()
    connection.close()
    return history

def get_monitors():
    connection = sqlite3.connect("monitor.db")
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    monitors = cur.execute("SELECT id, url FROM monitors")
    monitors = monitors.fetchall()
    connection.close()
    return monitors

def delete_monitor(monitor_id):
    connection = sqlite3.connect("monitor.db")
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("DELETE FROM monitors WHERE id = ?",  (monitor_id,))
    connection.commit()
    connection.close()
