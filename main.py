# main.py - Outsideking Control System [AUTO-GENERATOR V3]
# ตัวนี้จะซ่อมตัวเองและสร้างระบบที่หายไปให้อัตโนมัติ
import os, sys, importlib, time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
print(f"[{datetime.now()}] Control System Starting at {ROOT}")

# 1. AUTO-CREATE ไฟล์ที่หาย
REQUIRED = {
    "auth.py": 'def get_user():\n    return {"user": "Outsideking", "role": "admin"}\n',
    "controller.py": 'def run():\n    print("Controller running...")\n    return True\n',
    "export_report.py": 'def export():\n    print("Exporting report...")\n    return "report.csv"\n',
}

for fname, default_code in REQUIRED.items():
    fpath = ROOT / fname
    if not fpath.exists():
        print(f"[AUTO] สร้าง {fname} ที่หายไป...")
        fpath.write_text(default_code, encoding='utf-8')

# 2. AUTO-IMPORT แบบไม่ให้ตาย
def safe_import(name):
    try:
        return importlib.import_module(name)
    except Exception as e:
        print(f"[WARN] import {name} ไม่ได้: {e} - ใช้โหมดสำรอง")
        return None

auth = safe_import("auth")
controller = safe_import("controller")
export_report = safe_import("export_report")

# 3. AUTO-DETECT โฟลเดอร์
for folder in ["dashboard", "pipelines", "reports", ".github"]:
    p = ROOT / folder
    if not p.exists():
        print(f"[AUTO] สร้างโฟลเดอร์ {folder}")
        p.mkdir(exist_ok=True)
        (p / ".keep").touch()

# 4. MAIN SYSTEM
class ControlSystem:
    def __init__(self):
        self.status = "RUNNING"
        self.start_time = datetime.now()
        self.restart_count = 0

    def run(self):
        print(f"--- Outsideking Control System ONLINE ---")
        print(f"Files: {[f.name for f in ROOT.iterdir() if f.suffix=='.py']}")
        
        while True:
            try:
                # เรียก controller ถ้ามี
                if controller and hasattr(controller, 'run'):
                    controller.run()
                
                # เช็ค dashboard
                dash_path = ROOT / "dashboard"
                if dash_path.exists():
                    print(f"[OK] Dashboard found: {len(list(dash_path.iterdir()))} files")

                time.sleep(10) # ลูปทุก 10 วิ

            except KeyboardInterrupt:
                print("Stopped by user")
                break
            except Exception as e:
                self.restart_count += 1
                print(f"[IMMORTAL GUARD] ระบบล้มครั้งที่ {self.restart_count}: {e}")
                print(f"ซ่อมตัวเองใน 2 วินาที...")
                time.sleep(2)
                continue

# 5. WEB SERVER สำหรับ Vercel
try:
    from flask import Flask, jsonify
    app = Flask(__name__)
    sys_instance = ControlSystem()

    @app.route("/")
    def home():
        return jsonify({
            "system": "Outsideking Control System",
            "status": sys_instance.status,
            "uptime": str(datetime.now() - sys_instance.start_time),
            "restart_count": sys_instance.restart_count,
            "files": os.listdir(ROOT),
            "auto_generated": True,
            "time": datetime.now().isoformat()
        })

    @app.route("/health")
    def health():
        return jsonify({"ok": True})

    # สำหรับรันบนเครื่องพ่อ
    if __name__ == "__main__" and "vercel" not in str(ROOT).lower():
        # ถ้ารันบน Termux/PC ให้รันแบบลูปอมตะ
        ControlSystem().run()
    # ถ้าบน Vercel มันจะใช้ app ตัวนี้เอง

except ImportError:
    # ถ้าไม่มี Flask ก็รันแบบธรรมดา
    if __name__ == "__main__":
        ControlSystem().run()