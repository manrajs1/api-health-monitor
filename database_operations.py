import sqlite3
import datetime
import config

def add_monitor(url):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    
    # Using ? as a placeholder so the URL is treated as data instead of SQL code.
    # (url,) is a one-item tuple because execute expects the placeholder values as a collection.
    cur.execute("INSERT INTO monitors(url) VALUES (?)", (url, ))
    
    # Getting the id of the row that was just created
    monitor_id = cur.lastrowid
    
    # Saving the changes 
    connection.commit()
    connection.close()    
    return {"id" : monitor_id, "url":url}

def save_check(monitor_id, check_result):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    
     # Storing time in UTC so the backend uses one consistent timezone.
    current_time = datetime.datetime.now(datetime.timezone.utc )
    
     # Storing time in UTC so the backend uses one consistent timezone.
    timestamp = str(current_time)
    
    # Making sure the monitor_id exists in the monitors table before saving the check.
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
    
    # Saving the new check to the database.
    connection.commit()
    connection.close()

def get_check_history(monitor_id):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    
    # Finding all check rows connected to the given monitor id.
    rows = cur.execute("SELECT * FROM checks WHERE monitor_id = ?", (monitor_id,))
    
    # Fetching all matching rows into a Python list.
    history = rows.fetchall()
    
    connection.close()
    
    # Returning all check history for this monitor.
    return history

def get_monitors():
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    
    # Getting the id and url columns from all monitor rows.
    monitors = cur.execute("SELECT id, url FROM monitors")
    
    # Fetching all matching rows into a list.
    monitors = monitors.fetchall()
    
    connection.close()
    return monitors

def delete_monitor(monitor_id):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    
    # Enabling foreign keys so related check rows are deleted through ON DELETE CASCADE.
    cur.execute("PRAGMA foreign_keys = ON;")
    
    cur.execute("DELETE FROM monitors WHERE id = ?",  (monitor_id, ))
    
    # Saving the deletion
    connection.commit()
    connection.close()

def get_monitor(monitor_id: int):
    connection = sqlite3.connect(config.database_path)
    cur = connection.cursor()
    
    # Selecting the monitor row with the given id.
    monitor = cur.execute("SELECT id, url FROM monitors WHERE id = ?",(monitor_id, ))
    
    # Fetching one row because the monitor id is unique.
    result = monitor.fetchone()
    
    connection.close()
    return result