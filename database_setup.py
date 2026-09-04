import sqlite3
import config

def setup_database():   
    # Creating connection to the database
    connection = sqlite3.connect(config.database_path)
    # Creating messenger to send sql commands to the database
    cur = connection.cursor()
    
    cur.execute("PRAGMA foreign_keys = ON;")

    # Creating a new table with id as primary key and url with required text value
    cur.execute("CREATE TABLE IF NOT EXISTS monitors(id INTEGER PRIMARY KEY, url TEXT NOT NULL)")

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

    # Closing the connection
    connection.close()