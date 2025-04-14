import sqlite3

# This creates (or connects to) the smart_home.db file
def init_db():
    conn = sqlite3.connect('smart_home.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS device_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT NOT NULL,
            action TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert a scheduled device into the DB
def insert_schedule(device, action, time):
    conn = sqlite3.connect('smart_home.db')
    c = conn.cursor()
    c.execute('INSERT INTO device_schedule (device, action, time) VALUES (?, ?, ?)', (device, action, time))
    conn.commit()
    conn.close()

# Fetch all scheduled devices
def get_all_schedules():
    conn = sqlite3.connect('smart_home.db')
    c = conn.cursor()
    c.execute('SELECT * FROM device_schedule')
    schedules = c.fetchall()
    conn.close()
    return schedules
