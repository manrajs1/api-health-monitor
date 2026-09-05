import sqlite3
import config

def setup_database():   
    # Opening a connection to the database
    connection = sqlite3.connect(config.database_path)
    
    # Creating a cursor to send SQL commands through the connection
    cur = connection.cursor()
    
    # Enabling foreign key rules for this database connection
    cur.execute("PRAGMA foreign_keys = ON;")

    # Creating monitors table if it does not already exist
    cur.execute("CREATE TABLE IF NOT EXISTS monitors(id INTEGER PRIMARY KEY, url TEXT NOT NULL)")

    # monitor_id is a foreign key connected to monitors.id.
    # If a monitor is deleted, all checks connected to that monitor are also deleted.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS checks
        (
        id INTEGER PRIMARY KEY, 
        monitor_id INTEGER NOT NULL REFERENCES monitors(id) ON DELETE CASCADE , 
        status_code INTEGER, 
        response_time REAL NOT NULL, 
        timestamp TEXT NOT NULL, 
        up INTEGER NOT NULL, 
        error TEXT
        )
        """)

    # Saving the database changes
    connection.commit()
    
    # Closing the database connection
    connection.close()