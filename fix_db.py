import sqlite3

conn = sqlite3.connect('smart_home.db')  # Make sure this matches your DB filename
c = conn.cursor()

# Create the security_logs table
c.execute('''
  CREATE TABLE IF NOT EXISTS security_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp TEXT NOT NULL
  )
''')

conn.commit()
conn.close()

print("✅ security_logs table ensured!")
