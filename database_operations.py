import sqlite3
import datetime
import config

def add_monitor(url):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    # Enable foreign-key enforcement for this SQLite connection.
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("INSERT INTO monitors(url) VALUES (?)", (url, ))
    monitor_id = cur.lastrowid
    connection.commit()
    connection.close()
    return {"id" : monitor_id, "url":url}

def save_check(monitor_id, check_result):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    # Store check timestamps in UTC so the backend uses one consistent timezone.
    current_time = datetime.datetime.now(datetime.timezone.utc )
    timestamp = str(current_time)
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute('''
        INSERT INTO checks(monitor_id,
            status_code, 
            response_time, 
            timestamp, 
            up, 
            error) 
            VALUES (?,?,?,?,?,?)
    ''',    (monitor_id, check_result["status_code"],
             check_result["response_time"],
            timestamp, check_result["up"],
            check_result['error'])
    )
    connection.commit()
    connection.close()

def get_check_history(monitor_id):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    rows = cur.execute('''
        SELECT * FROM checks WHERE monitor_id = ?
    ''', (monitor_id,))
    history = rows.fetchall()
    connection.close()
    return history

def get_monitors():
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    monitors = cur.execute("SELECT id, url FROM monitors")
    monitors = monitors.fetchall()
    connection.close()
    return monitors

def delete_monitor(monitor_id):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("DELETE FROM monitors WHERE id = ?",  (monitor_id, ))
    connection.commit()
    connection.close()

def get_monitor(monitor_id: int):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    monitor = cur.execute("SELECT id, url FROM monitors WHERE id = ?",(monitor_id, ))
    result = monitor.fetchone()
    connection.close()
    return result