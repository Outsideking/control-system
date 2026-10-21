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