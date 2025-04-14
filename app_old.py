from flask import Flask , render_template,  jsonify
import random

app = Flask(__name__)

@app.route('/temperature')
def temperature():
    temp = random.randint(20 , 30)  # Just an example, replace with real sensor data if needed
    return jsonify({"temperature": temp, "success": True})

@app.route('/lights')
def lights():
    return jsonify({"lights": "ON" , "success": True})

@app.route('/status')
def get_status():
    return jsonify({"system": "OK", "success": True})

@app.route('/')
def home():
    return render_template('index.html')

print(app.url_map)

if __name__ == "_main_":
    app.run(debug=True, use_reloader=True)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulating light status (Initially OFF)
light_status = "OFF"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/lights", methods=["GET"])
def control_lights():
    global light_status
    state = request.args.get("state")

    print(f"Raw state received: {state}")

    if state  and state.lower() in ["on", "off"]:
        light_status = state.upper()
        print(f"Updated light success: {light_status}")
        return jsonify({"success": True, "lights": light_status})
    
    print("Invalid state receiced!")
    return jsonify({"success": False, "error": "Invalid state"}), 400

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({"lights": light_status})

@app.route("/temperature", methods=["GET"])
def get_temperature():
    return jsonify({"temperature": 25})

if __name__ == "_main_":
    app.run(debug=True)

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '_main_':
    app.run(debug=True)