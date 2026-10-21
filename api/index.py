from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return jsonify({
        "status": "ONLINE",
        "system": "Outsideking Control System - FIXED",
        "path": path,
        "time": datetime.now().isoformat(),
        "url": "https://control-system-peach.vercel.app"
    })

# สำคัญมากสำหรับ Vercel
def handler(request):
    return app(request)
from controller import status, broadcast, send_command

@app.route("/control")
def control_panel():
    return status()

@app.route("/control/broadcast/<action>")
def control_all(action):
    return broadcast(action)

@app.route("/control/send/<app_name>/<action>")
def control_one(app_name, action):
    return send_command(app_name, action)