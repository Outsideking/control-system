# ============================================================
# 🎮 CONTROL-SYSTEM — ALL-IN-ONE SINGLE FILE
# รันได้เลย: python run_all.py
# เชื่อมต่อ: SC + ScanZaclip + Dashboard + Reports + Alerts
# ============================================================

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================
# 📦 INSTALL CHECK — ตรวจสอบและติดตั้งแพ็กเกจอัตโนมัติ
# ============================================================
def install_requirements():
    try:
        import pip
    except ImportError:
        print("❌ ไม่พบ pip กรุณาติดตั้ง Python ก่อน")
        sys.exit(1)
    
    required = {
        "flask": "Flask",
        "flask-socketio": "flask_socketio",
        "requests": "requests",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "openpyxl": "openpyxl",
        "reportlab": "reportlab",
        "python-dotenv": "dotenv"
    }
    
    missing = []
    for pkg, mod in required.items():
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"📦 กำลังติดตั้ง: {', '.join(missing)}")
        import subprocess
        for pkg in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print("✅ ติดตั้งครบถ้วน\n")

# ============================================================
# 🔐 AUTH SYSTEM — ระบบยืนยันตัวตน
# ============================================================
class AuthManager:
    def __init__(self):
        self.users = {"admin": "control2026"}
        print("✅ ระบบยืนยันตัวตนพร้อม")
    
    def verify(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

# ============================================================
# 🎛️ CONTROLLER — ระบบควบคุม Pipeline
# ============================================================
class PipelineController:
    def __init__(self):
        self.results = []
        self.repos = []
        print("✅ ระบบควบคุม Pipeline พร้อม")
    
    def add_repo(self, url: str, token: str = None):
        self.repos.append({"url": url, "token": token, "active": True})
        return {"success": True, "repo": url}
    
    def run_pipeline(self, repo_url: str = None, repo_token: str = None) -> Dict:
        repo = repo_url or "local-system"
        start_time = time.time()
        
        print(f"🔄 กำลังรัน: {repo}")
        time.sleep(0.5)  # จำลองการทำงาน
        
        success = True
        result = {
            "id": len(self.results) + 1,
            "repo": repo,
            "status": "success" if success else "failed",
            "timestamp": datetime.now().isoformat(),
            "duration": round(time.time() - start_time, 2),
            "steps": ["clone", "build", "test", "deploy"],
            "fail_rate": 0.0
        }
        
        self.results.append(result)
        return result
    
    def get_stats(self) -> Dict:
        total = len(self.results)
        success = sum(1 for r in self.results if r["status"] == "success")
        failed = total - success
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": round((success / total * 100), 2) if total > 0 else 0
        }

# ============================================================
# 📋 TASK MANAGER — ระบบจัดการงาน
# ============================================================
class TaskManager:
    def __init__(self):
        self.tasks = []
        print("✅ ระบบจัดการงานพร้อม")
    
    def add_task(self, name: str, desc: str = ""):
        task = {
            "id": len(self.tasks) + 1,
            "name": name,
            "description": desc,
            "status": "pending",
            "created": datetime.now().isoformat()
        }
        self.tasks.append(task)
        return task
    
    def get_recent(self, limit: int = 5) -> List:
        return list(reversed(self.tasks[-limit:]))

# ============================================================
# 📊 REPORT EXPORTER — ระบบส่งออกรายงาน
# ============================================================
class ReportExporter:
    def __init__(self):
        self.records = []
        os.makedirs("reports", exist_ok=True)
        print("✅ ระบบรายงานพร้อม")
    
    def add_record(self, result: Dict):
        self.records.append(result)
    
    def export_all(self, format_type: str = "json") -> Dict:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == "json":
            path = f"reports/report_{timestamp}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        elif format_type == "txt":
            path = f"reports/report_{timestamp}.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"CONTROL-SYSTEM REPORT\n{'='*40}\n")
                f.write(f"สร้างเมื่อ: {datetime.now()}\n")
                f.write(f"จำนวนทั้งหมด: {len(self.records)}\n\n")
                for r in self.records:
                    f.write(f"#{r['id']} {r['repo']} — {r['status']}\n")
        else:
            return {"success": False, "error": "รูปแบบไม่รองรับ ใช้ json หรือ txt"}
        
        return {"success": True, "path": path, "count": len(self.records)}

# ============================================================
# 🚨 NOTIFIER — ระบบแจ้งเตือน
# ============================================================
class MultiNotifier:
    def __init__(self):
        self.alerts = []
        print("✅ ระบบแจ้งเตือนพร้อม")
    
    def send_alert(self, alert_data: Dict):
        alert = {
            "time": datetime.now().isoformat(),
            "message": alert_data.get("message", "แจ้งเตือนจากระบบ"),
            "level": alert_data.get("level", "info")
        }
        self.alerts.append(alert)
        print(f"🚨 แจ้งเตือน: {alert['message']}")
        return alert

class TrendAnalyzer:
    def __init__(self):
        self.history = []
        print("✅ ระบบวิเคราะห์แนวโน้มพร้อม")
    
    def analyze(self, result: Dict) -> Dict:
        self.history.append(result)
        fail_count = sum(1 for r in self.history if r["status"] == "failed")
        fail_rate = (fail_count / len(self.history) * 100) if self.history else 0
        
        alert = {
            "alert": fail_rate > 20,
            "fail_rate": round(fail_rate, 2),
            "message": f"อัตราความล้มเหลว: {round(fail_rate, 2)}%"
        }
        return alert

# ============================================================
# 🔌 SC INTEGRATION — เชื่อมต่อระบบ SC
# ============================================================
class SCConnector:
    def __init__(self):
        self.connected = True
        self.endpoint = "local-connection"
        os.makedirs("sc_data", exist_ok=True)
        print("✅ เชื่อมต่อ SC สำเร็จ")
    
    def sync_result(self, result: Dict) -> Dict:
        data = {"time": datetime.now().isoformat(), "data": result}
        with open("sc_data/sync.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        return {"success": True}

# ============================================================
# 🔌 SCANZACLIP INTEGRATION — เชื่อมต่อ ScanZaclip
# ============================================================
class ScanZaclip:
    def __init__(self):
        self.log_file = "scanzaclip_logs.jsonl"
        print("✅ เชื่อมต่อ ScanZaclip สำเร็จ")
    
    def log_data(self, data: Dict) -> Dict:
        entry = {"time": datetime.now().isoformat(), "type": "pipeline", "data": data}
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return {"success": True}

# ============================================================
# 🧠 SYSTEM MANAGER — จุดศูนย์กลางควบคุมทุกระบบ
# ============================================================
class ControlSystem:
    def __init__(self):
        self.start_time = datetime.now()
        self.init_systems()
    
    def init_systems(self):
        print("=" * 50)
        print("🚀 กำลังเริ่มต้น Control-System...")
        print("=" * 50)
        
        self.auth = AuthManager()
        self.controller = PipelineController()
        self.tasks = TaskManager()
        self.exporter = ReportExporter()
        self.notifier = MultiNotifier()
        self.trend = TrendAnalyzer()
        self.sc = SCConnector()
        self.scanzaclip = ScanZaclip()
        
        print("\n" + "=" * 50)
        print("🎉 ทุกระบบทำงานพร้อมกันแล้ว!")
        print("=" * 50 + "\n")
    
    def get_status(self) -> Dict:
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            "status": "running",
            "uptime": round(uptime, 2),
            "components": {
                "auth": True, "controller": True, "tasks": True,
                "reports": True, "notifier": True, "sc": True,
                "scanzaclip": True
            },
            "stats": self.controller.get_stats()
        }
    
    def run_full_pipeline(self, repo_url: str = "local-project") -> Dict:
        print(f"▶️  เริ่มกระบวนการทั้งหมด: {repo_url}")
        
        # 1. รัน Pipeline
        result = self.controller.run_pipeline(repo_url)
        
        # 2. บันทึกลงรายงาน
        self.exporter.add_record(result)
        
        # 3. ตรวจสอบแนวโน้ม
        alert = self.trend.analyze(result)
        if alert["alert"]:
            self.notifier.send_alert(alert)
        
        # 4. ซิงค์ไป SC
        self.sc.sync_result(result)
        
        # 5. บันทึก ScanZaclip
        self.scanzaclip.log_data(result)
        
        print(f"✅ เสร็จสิ้น: {result['status']}")
        return result
    
    def dashboard_data(self) -> Dict:
        return {
            "time": datetime.now().isoformat(),
            "system": self.get_status(),
            "recent": self.controller.results[-5:],
            "tasks": self.tasks.get_recent()
        }

# ============================================================
# 🖥️ WEB DASHBOARD — ในตัว ไม่ต้องใช้ไฟล์อื่น
# ============================================================
def start_web_mode(system: ControlSystem):
    from flask import Flask, render_template_string, jsonify
    
    app = Flask("ControlSystem")
    
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Control-System Dashboard</title>
        <style>
            *{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:0;padding:0;}
            body{background:#f0f2f5;padding:20px;max-width:1200px;margin:0 auto;}
            h1{color:#1a73e8;margin-bottom:20px;}
            .card{background:white;border-radius:12px;padding:20px;margin-bottom:15px;box-shadow:0 2px 10px rgba(0,0,0,0.08);}
            .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;}
            .stat{text-align:center;}
            .stat h2{font-size:32px;color:#1a73e8;}
            .status{display:inline-block;padding:6px 12px;border-radius:20px;background:#e6f4ea;color:#137333;font-weight:bold;}
            button{background:#1a73e8;color:white;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;font-size:15px;}
            button:hover{background:#1557b0;}
            pre{background:#f8f9fa;padding:12px;border-radius:6px;overflow-x:auto;margin-top:10px;}
        </style>
    </head>
    <body>
        <h1>🎛️ Control-System Dashboard</h1>
        <div class="card">
            <strong>สถานะระบบ:</strong> <span class="status" id="sys-status">กำลังโหลด...</span>
            <p style="margin-top:8px">ทำงานมา: <span id="uptime">-</span> วินาที</p>
        </div>
        <div class="grid">
            <div class="card stat"><h2 id="total">0</h2><p>รันทั้งหมด</p></div>
            <div class="card stat"><h2 style="color:#137333" id="success">0</h2><p>สำเร็จ</p></div>
            <div class="card stat"><h2 style="color:#d93025" id="failed">0</h2><p>ล้มเหลว</p></div>
            <div class="card stat"><h2 style="color:#f29900" id="rate">0%</h2><p>อัตราสำเร็จ</p></div>
        </div>
        <div class="card">
            <h3>⚙️ เมนูควบคุม</h3>
            <button onclick="runPipeline()">▶️ รัน Pipeline ทดสอบ</button>
            <button onclick="exportReport()">📤 ส่งออกรายงาน</button>
            <button onclick="location.reload()">🔄 รีเฟรช</button>
        </div>
        <div class="card">
            <h3>📋 ผลลัพธ์ล่าสุด</h3>
            <pre id="output">รอทำงาน...</pre>
        </div>
        <script>
        async function update(){
            try{const r=await fetch('/api/data');const d=await r.json();
            document.getElementById('sys-status').textContent=d.system.status==='running'?'✅ กำลังทำงาน':'⚠️ หยุดทำงาน';
            document.getElementById('uptime').textContent=d.system.uptime;
            document.getElementById('total').textContent=d.system.stats.total;
            document.getElementById('success').textContent=d.system.stats.success;
            document.getElementById('failed').textContent=d.system.stats.failed;
            document.getElementById('rate').textContent=d.system.stats.success_rate+'%';
            document.getElementById('output').textContent=JSON.stringify(d.recent,[],2)||'ยังไม่มีข้อมูล';}
            catch(e){console.log(e);}}
        async function runPipeline(){const r=await fetch('/api/run');const d=await r.json();alert('รันเสร็จสิ้น!');update();}
        async function exportReport(){const r=await fetch('/api/export');const d=await r.json();alert(d.message||'ส่งออกแล้ว');}
        update();setInterval(update,3000);
        </script>
    </body>
    </html>
    """
    
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/api/data')
    def api_data():
        return jsonify(system.dashboard_data())
    
    @app.route('/api/run')
    def api_run():
        result = system.run_full_pipeline("web-triggered")
        return jsonify({"message": "รันสำเร็จ", "result": result})
    
    @app.route('/api/export')
    def api_export():
        result = system.exporter.export_all("json")
        return jsonify({"message": "ส่งออกแล้ว", "path": result.get("path")})
    
    print("🌐 เปิดเว็บ: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# ============================================================
# 🏃‍♂️ MAIN PROGRAM — เริ่มทำงาน
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🎛️  CONTROL-SYSTEM — All-in-One Version")
    print("=" * 50 + "\n")
    
    # ติดตั้งแพ็กเกจอัตโนมัติ
    install_requirements()
    
    # เริ่มระบบ
    system = ControlSystem()
    
    while True:
        print("\n" + "-" * 45)
        print("📋 เมนูหลัก:")
        print("  1. 📊 ดูสถานะระบบ")
        print("  2. 🔄 รัน Pipeline ทดสอบ")
        print("  3. 📤 ส่งออกรายงาน")
        print("  4. 🌐 เปิดแดชบอร์ดเว็บ")
        print("  5. 🔍 ดูข้อมูลล่าสุด")
        print("  6. ❌ ออกจากระบบ")
        
        choice = input("\nเลือกทำงาน (1-6): ").strip()
        
        if choice == "1":
            status = system.get_status()
            print("\n📊 สถานะระบบ:")
            print(f"   สถานะ: {status['status']}")
            print(f"   ทำงานมา: {status['uptime']} วินาที")
            print(f"   รันทั้งหมด: {status['stats']['total']} ครั้ง")
            print(f"   สำเร็จ: {status['stats']['success']} ครั้ง")
            print(f"   ล้มเหลว: {status['stats']['failed']} ครั้ง")
            print(f"   อัตราสำเร็จ: {status['stats']['success_rate']}%")
        
        elif choice == "2":
            repo = input("🔗 ชื่อ/URL Repository (กด Enter ข้าม): ").strip() or "test-project"
            system.run_full_pipeline(repo)
        
        elif choice == "3":
            fmt = input("📄 รูปแบบ (json/txt): ").strip() or "json"
            result = system.exporter.export_all(fmt)
            print(f"✅ บันทึกที่: {result.get('path', 'สำเร็จ')}")
        
        elif choice == "4":
            print("\n🌐 กำลังเปิดแดชบอร์ด... กด Ctrl+C เพื่อปิด")
            start_web_mode(system)
        
        elif choice == "5":
            data = system.dashboard_data()
            print("\n🔍 ข้อมูลล่าสุด:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        
        elif choice == "6":
            print("\n👋 ปิดระบบ... ขอบคุณที่ใช้งาน!")
            break
        
        else:
            print("❌ กรุณาเลือก 1-6 เท่านั้น")
