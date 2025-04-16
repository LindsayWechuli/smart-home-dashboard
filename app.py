from flask import Flask, render_template, jsonify, request
from database import init_db, insert_schedule, get_all_schedules

app = Flask(__name__)
init_db()

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')

# 🌡️ Temperature API
@app.route('/temperature')
def temperature():
    return jsonify({'temperature': 25})  # Simulated value

# 💡 Lights Control
@app.route('/lights/<state>', methods=['POST'])
def control_lights(state):
    if state not in ["on", "off"]:
        return jsonify({"status": "Invalid state"}), 400
    return jsonify({"status": f"Lights turned {state}"})

# ⚡ Energy Monitoring
@app.route('/api/energy-usage')
def energy_usage():
    return jsonify({'usage': '350W'})  # Simulated usage

# 🧠 System Status
@app.route('/system-status')
def system_status():
    return jsonify(status="All systems functional")

# 📅 Device Scheduler (accepting JSON from script.js)
@app.route('/schedule-device', methods=['POST'])
def schedule_device():
    data = request.get_json()
    device_name = data.get('device')
    schedule_time = data.get('time')
    action = data.get('action')

    if not device_name or not schedule_time or not action:
        return jsonify({"error": "Missing data"}), 400

    insert_schedule(device_name, schedule_time, action)

    print(f"✅ Scheduled: {device_name} to turn {action} at {schedule_time}")
    return jsonify({"message": "Schedule saved successfully"}), 200

@app.route('/get-schedules', methods=['GET'])
def get_schedules():
    schedules = get_all_schedules()
    result = []
    for schedule in schedules:
        # Skip the ID field if present: (id, device, time, action)
        if len(schedule) == 4:
            _, device, time, action = schedule
        else:
            device, time, action = schedule  # fallback if only 3 items
        result.append({
            'device': device,
            'time': time,
            'action': action
        })
    return jsonify(result)

@app.route('/lock/<state>', methods=['POST'])
def control_lock(state):
    if state not in ['lock', 'unlock']:
        return jsonify({"error": "Invalid lock state"}), 400

    print(f"{state.capitalize()}ing the door...")
    return jsonify({"message": f"Door {state}ed!"})


# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
