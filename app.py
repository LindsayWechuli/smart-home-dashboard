from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from datetime import datetime
from functools import wraps
import sqlite3
import os
print("📁 Current working directory:", os.getcwd())


app = Flask(__name__)
app.secret_key = 'Wechuli'  # Replace with a real secret key!


# 📦 Database Setup
def get_db_connection():
    conn = sqlite3.connect('smart_home.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        # Users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                role TEXT
            )
        ''')

        # Device schedules
        c.execute('''
            CREATE TABLE IF NOT EXISTS device_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT NOT NULL,
                action TEXT NOT NULL,
                schedule_time TEXT NOT NULL,
                created_by TEXT NOT NULL
            )
        ''')

        # Device statuses
        c.execute('''
            CREATE TABLE IF NOT EXISTS device_statuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT NOT NULL,
                status TEXT NOT NULL,
                last_updated TEXT NOT NULL
            )
        ''')

        # Energy monitoring logs
        c.execute('''
            CREATE TABLE IF NOT EXISTS energy_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT NOT NULL,
                energy_usage REAL NOT NULL,
                log_time TEXT NOT NULL
            )
        ''')

        # Security logs
        c.execute('''
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()


# 🪵 Event Logger
def log_event(action, category="general"):
    try:
        with get_db_connection() as conn:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                'INSERT INTO security_logs (device, action, timestamp) VALUES (?, ?, ?)',
                (category, action, timestamp)
            )
            conn.commit()
    except Exception as e:
        print(f"Log error: {e}")


# 🛡️ Access Control
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                flash("Access denied: Insufficient permissions.")
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 🏠 Home
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    role = session.get('role', 'guest')
    return render_template('index.html', role=role)


# 💡 Light
@app.route('/lights/<state>', methods=['POST'])
def control_lights(state):
    if state not in ["on", "off"]:
        return jsonify({"status": "Invalid state"}), 400
    try:
        log_event(f"Turned lights {state}", category="lighting")
    except Exception as e:
        print(f"❌ Logging error: {e}")
        return jsonify({"status": "Logging failed"}), 500
    return jsonify({"status": f"Lights turned {state}"}), 200


# ⚡ Energy Monitoring
@app.route('/api/energy-usage')
def energy_usage():
    return jsonify({'usage': '350W'})  # Simulated


# 🧠 System Status
@app.route('/system-status')
def system_status():
    return jsonify(status="All systems functional")

# 🌡️ Temperature Endpoint
@app.route('/temperature')
def get_temperature():
    # Simulate a temperature readout
    simulated_temp = 24.5  # You can randomize or pull from sensors later!
    return jsonify({"temperature": simulated_temp})


# 📅 Device Scheduling
@app.route('/schedule-device', methods=['POST'])
def schedule_device():
    data = request.get_json()
    device_name = data.get('device')
    schedule_time = data.get('time')
    action = data.get('action')

    if not all([device_name, schedule_time, action]):
        return jsonify({"error": "Missing data"}), 400

    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO device_schedules (device_name, schedule_time, action, created_by)
                VALUES (?, ?, ?, ?)
            ''', (device_name, schedule_time, action, session.get('user', 'unknown')))
            conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Schedule saved successfully"}), 200


@app.route('/get-schedules', methods=['GET'])
def get_schedules():
    with get_db_connection() as conn:
        schedules = conn.execute('SELECT device_name, schedule_time, action FROM device_schedules').fetchall()
    return jsonify([dict(s) for s in schedules])


# 🔐 Lock Control
@app.route('/lock/<state>', methods=['POST'])
def control_lock(state):
    if state not in ['lock', 'unlock']:
        return jsonify({"error": "Invalid lock state"}), 400
    return jsonify({"message": f"Door {state}ed!"})


# 🔑 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as conn:
            cursor = conn.execute("SELECT username, password, role FROM users WHERE username=? AND password=?",
                                  (username, password))
            user = cursor.fetchone()

        if user:
            session['user'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')


# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# 🚪 Bedroom Lock - Admin Only
@app.route('/lock-bedroom/<state>', methods=['POST'])
@role_required(['admin'])
def lock_bedroom(state):
    if state not in ['lock', 'unlock']:
        return jsonify({"error": "Invalid state"}), 400
    return jsonify({"message": f"Bedroom door {state}ed!"})


# 🚀 Start App
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
