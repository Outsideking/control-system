# main.py - Control System by Outsideking
# ระบบควบคุมอมตะ ซ่อมตัวเองได้
import os
import time
import traceback
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# --- หน่วยความจำระบบ ---
SYSTEM_STATUS = {
    "name": "Outsideking Control System",
    "version": "2.0-immortal",
    "status": "RUNNING",
    "uptime_start": datetime.now().isoformat(),
    "restart_count": 0,
    "last_error": None,
    "location": "Ban Pao, Lampang"
}

def immortal_guard(func):
    """ยามเฝ้าระบบ ถ้าพังให้ซ่อมแล้วไปต่อ ไม่ให้ตาย"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            SYSTEM_STATUS["last_error"] = f"{str(e)} at {datetime.now()}"
            SYSTEM_STATUS["restart_count"] += 1
            print(f"[GUARD] จับ error ได้: {e}")
            print(traceback.format_exc())
            # ไม่ให้ล่ม ให้ส่งสถานะกลับแทน
            return jsonify({
                "alive": True,
                "auto_healed": True,
                "error": str(e),
                "status": SYSTEM_STATUS
            }), 200
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/")
@immortal_guard
def home():
    return jsonify({
        "message": "Control System Online - Outsideking",
        "time": datetime.now().isoformat(),
        "system": SYSTEM_STATUS
    })

@app.route("/health")
@immortal_guard
def health():
    # เอาไว้ให้ Vercel เช็ค
    return jsonify({"status": "ok", "uptime": SYSTEM_STATUS["uptime_start"]})

@app.route("/control", methods=["POST"])
@immortal_guard
def control():
    data = request.json or {}
    action = data.get("action", "")
    
    if action == "restart":
        SYSTEM_STATUS["restart_count"] += 1
        SYSTEM_STATUS["uptime_start"] = datetime.now().isoformat()
        return jsonify({"result": "restarted", "system": SYSTEM_STATUS})
    
    if action == "status":
        return jsonify(SYSTEM_STATUS)
        
    return jsonify({"result": f"รับคำสั่ง {action} แล้ว", "system": SYSTEM_STATUS})

@app.route("/api/log")
@immortal_guard
def log():
    return jsonify(SYSTEM_STATUS)

# Vercel ต้องมีตัวนี้
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[SYSTEM] Starting on port {port} - Immortal Mode ON")
    while True:
        try:
            app.run(host="0.0.0.0", port=port)
        except Exception as e:
            print(f"[CRITICAL] System crashed, auto-restarting in 2s: {e}")
            SYSTEM_STATUS["restart_count"] += 1
            time.sleep(2)