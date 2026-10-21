from flask import Flask, jsonify
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "ONLINE", "system": "Outsideking Control System", "time": datetime.now().isoformat()})

@app.route("/health")
def health():
    return jsonify({"ok": True})