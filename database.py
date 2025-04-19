import sqlite3
import hashlib
import json

DB_PATH = "smart_home.db"

def get_conn():
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    # schedules table
    c.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      device_name TEXT NOT NULL,
      schedule_time TEXT NOT NULL,
      action TEXT NOT NULL
    )
    """)

    # users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      role TEXT NOT NULL,
      allowed_devices TEXT NOT NULL DEFAULT '[]'
    )
    """)

    conn.commit()
    conn.close()

# ──────── user helpers ───────────────────────────────────────────────────────

def insert_user(username, password, role="staff", allowed_devices=None):
    """Create a user with a SHA‑256 password hash and a JSON list of allowed devices."""
    allowed = allowed_devices or []
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_conn()
    c = conn.cursor()
    c.execute(
      "INSERT INTO users (username, password_hash, role, allowed_devices) VALUES (?, ?, ?, ?)",
      (username, pw_hash, role, json.dumps(allowed))
    )
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
      "SELECT id, username, password_hash, role, allowed_devices "
      "FROM users WHERE username = ?",
      (username,)
    )
    row = c.fetchone()
    conn.close()
    if not row:
      return None
    uid, user, pw_hash, role, allowed = row
    return {
      "id": uid,
      "username": user,
      "password_hash": pw_hash,
      "role": role,
      "allowed_devices": json.loads(allowed)
    }

def get_all_users():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, username, role, allowed_devices FROM users")
    rows = c.fetchall()
    conn.close()
    return [
      {"id": r[0], "username": r[1], "role": r[2], "allowed_devices": json.loads(r[3])}
      for r in rows
    ]

# ──────── schedule helpers ────────────────────────────────────────────────────

def insert_schedule(device_name, schedule_time, action):
    """Add a new schedule entry into schedules."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
      "INSERT INTO schedules (device_name, schedule_time, action) VALUES (?, ?, ?)",
      (device_name, schedule_time, action)
    )
    conn.commit()
    conn.close()

def get_all_schedules():
    """Fetch all scheduled tasks."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT device_name, schedule_time, action FROM schedules")
    rows = c.fetchall()
    conn.close()
    return rows
