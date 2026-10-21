# ============================================================
# 🎮 CONTROL-SYSTEM — MAIN PROGRAM (Fixed & Unified)
# เชื่อมต่อ: SC, ScanZaclip, Pipelines, Reports, Dashboard, Notifier
# ============================================================

import os
import sys
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# โหลดตัวแปรสภาพแวดล้อม
load_dotenv()

# เพิ่ม path เพื่อให้ import โมดูลได้ถูกต้อง
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ============================================================
# 📥 IMPORT MODULES — ทุกระบบ
# ============================================================
try:
    from auth import AuthManager
    from controller import PipelineController
    from tasks import TaskManager
    from export_report import ReportExporter
    from notifier_multi import MultiNotifier
    from notifier_trend import TrendAnalyzer
    
    # ระบบภายนอกที่ต้องการเชื่อมต่อ
    try:
        from sc_integration import SCConnector
        print("✅ SC Module โหลดสำเร็จ")
    except ImportError:
        SCConnector = None
        print("⚠️  SC Module ไม่พบ — สร้างโครงเปล่าไว้ทำงานต่อได้")
    
    try:
        from scanzaclip import ScanZaclip
        print("✅ ScanZaclip Module โหลดสำเร็จ")
    except ImportError:
        ScanZaclip = None
        print("⚠️  ScanZaclip Module ไม่พบ — สร้างโครงเปล่าไว้ทำงานต่อได้")
    
    print("✅ ทุกโมดูลหลักโหลดสำเร็จ\n")
    
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการโหลดโมดูล: {e}")
    sys.exit(1)

# ============================================================
# 🌐 SYSTEM MANAGER — รวมทุกระบบเข้าด้วยกัน
# ============================================================
class SystemManager:
    """จัดการทุกระบบทำงานร่วมกัน — จุดศูนย์กลางการควบคุม"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.systems = {}
        self.status = "idle"
        self.init_systems()
    
    def init_systems(self):
        """เริ่มต้นทุกระบบทีละตัว"""
        print("=" * 60)
        print("🚀 กำลังเริ่มต้นระบบทั้งหมด...")
        print("=" * 60)
        
        # 1. ระบบยืนยันตัวตน
        try:
            self.systems["auth"] = AuthManager()
            print("✅ ระบบยืนยันตัวตน — พร้อมใช้งาน")
        except Exception as e:
            print(f"⚠️  ระบบยืนยันตัวตน: {e}")
            self.systems["auth"] = None
        
        # 2. ระบบควบคุม Pipeline
        try:
            self.systems["controller"] = PipelineController()
            print("✅ ระบบควบคุม Pipeline — พร้อมใช้งาน")
        except Exception as e:
            print(f"⚠️  ระบบควบคุม Pipeline: {e}")
            self.systems["controller"] = None
        
        # 3. ระบบจัดการงาน
        try:
            self.systems["tasks"] = TaskManager()
            print("✅ ระบบจัดการงาน — พร้อมใช้งาน")
        except Exception as e:
            print(f"⚠️  ระบบจัดการงาน: {e}")
            self.systems["tasks"] = None
        
        # 4. ระบบรายงาน
        try:
            self.systems["exporter"] = ReportExporter()
            print("✅ ระบบรายงาน — พร้อมใช้งาน")
        except Exception as e:
            print(f"⚠️  ระบบรายงาน: {e}")
            self.systems["exporter"] = None
        
        # 5. ระบบแจ้งเตือน
        try:
            self.systems["notifier"] = MultiNotifier()
            self.systems["trend"] = TrendAnalyzer()
            print("✅ ระบบแจ้งเตือน — พร้อมใช้งาน")
        except Exception as e:
            print(f"⚠️  ระบบแจ้งเตือน: {e}")
            self.systems["notifier"] = None
            self.systems["trend"] = None
        
        # 6. เชื่อมต่อ SC (ถ้ามี)
        if SCConnector:
            try:
                self.systems["sc"] = SCConnector()
                print("✅ ระบบ SC — เชื่อมต่อสำเร็จ")
            except Exception as e:
                print(f"⚠️  ระบบ SC: {e}")
                self.systems["sc"] = None
        else:
            print("ℹ️  ระบบ SC — รอการติดตั้งไฟล์ sc_integration.py")
            self.systems["sc"] = None
        
        # 7. เชื่อมต่อ ScanZaclip (ถ้ามี)
        if ScanZaclip:
            try:
                self.systems["scanzaclip"] = ScanZaclip()
                print("✅ ระบบ ScanZaclip — เชื่อมต่อสำเร็จ")
            except Exception as e:
                print(f"⚠️  ระบบ ScanZaclip: {e}")
                self.systems["scanzaclip"] = None
        else:
            print("ℹ️  ระบบ ScanZaclip — รอการติดตั้งไฟล์ scanzaclip.py")
            self.systems["scanzaclip"] = None
        
        print("\n" + "=" * 60)
        print("🎉 ทุกระบบเริ่มต้นเสร็จสมบูรณ์")
        print("=" * 60)
        self.status = "running"
    
    def get_status(self):
        """สถานะทุกระบบ"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        return {
            "status": self.status,
            "uptime_seconds": round(uptime, 2),
            "systems": {name: (inst is not None) for name, inst in self.systems.items()}
        }
    
    def run_pipeline(self, repo_url, repo_token=None):
        """รัน pipeline — เรียกผ่านจุดศูนย์กลาง"""
        if not self.systems["controller"]:
            return {"success": False, "error": "Controller ไม่พร้อมใช้งาน"}
        
        print(f"\n🔄 กำลังรัน Pipeline: {repo_url}")
        result = self.systems["controller"].run_pipeline(repo_url, repo_token)
        
        # บันทึกผลลงรายงาน
        if self.systems["exporter"]:
            self.systems["exporter"].add_record(result)
        
        # ตรวจสอบแนวโน้มและแจ้งเตือน
        if self.systems["trend"] and result.get("status") == "failed":
            alert = self.systems["trend"].analyze(result)
            if alert.get("alert") and self.systems["notifier"]:
                self.systems["notifier"].send_alert(alert)
        
        # ถ้ามี SC ให้ส่งข้อมูลไปด้วย
        if self.systems["sc"]:
            self.systems["sc"].sync_result(result)
        
        # ถ้ามี ScanZaclip ให้บันทึกข้อมูล
        if self.systems["scanzaclip"]:
            self.systems["scanzaclip"].log_data(result)
        
        return result
    
    def export_all_reports(self, format_type="excel"):
        """ส่งออกรายงานทั้งระบบ"""
        if not self.systems["exporter"]:
            return {"success": False, "error": "Report module ไม่พร้อมใช้งาน"}
        
        return self.systems["exporter"].export_all(format_type)
    
    def dashboard_data(self):
        """ข้อมูลสำหรับแดชบอร์ด"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "system_status": self.get_status(),
            "recent_tasks": [],
            "pipeline_stats": {}
        }
        
        if self.systems["tasks"]:
            data["recent_tasks"] = self.systems["tasks"].get_recent()
        
        if self.systems["controller"]:
            data["pipeline_stats"] = self.systems["controller"].get_stats()
        
        return data


# ============================================================
# 🖥️ FLASK WEB SERVER — Dashboard & API
# ============================================================
def create_app():
    from flask import Flask, render_template, jsonify, request
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # สร้าง instance ระบบ
    system = SystemManager()
    
    @app.route('/')
    def index():
        return render_template('index.html', system=system.get_status())
    
    @app.route('/api/status')
    def api_status():
        return jsonify(system.get_status())
    
    @app.route('/api/dashboard')
    def api_dashboard():
        return jsonify(system.dashboard_data())
    
    @app.route('/api/run', methods=['POST'])
    def api_run():
        data = request.json
        result = system.run_pipeline(
            data.get('repo_url'),
            data.get('repo_token')
        )
        return jsonify(result)
    
    @app.route('/api/export/<format_type>')
    def api_export(format_type):
        result = system.export_all_reports(format_type)
        return jsonify(result)
    
    return app, system


# ============================================================
# 🏃‍♂️ RUN — เริ่มทำงาน
# ============================================================
if __name__ == "__main__":
    print("\n🎮 CONTROL-SYSTEM — เวอร์ชันแก้ไขแล้ว")
    print("🔗 เชื่อมต่อ: SC + ScanZaclip + ทุกระบบ\n")
    
    # ตรวจสอบโหมดการทำงาน
    mode = input("เลือกโหมด (1=ทดสอบคอนโซล, 2=รันเว็บเซิร์ฟเวอร์): ").strip()
    
    if mode == "1":
        # โหมดทดสอบคอนโซล
        system = SystemManager()
        
        while True:
            print("\n" + "-" * 50)
            print("เมนูหลัก:")
            print("  1. 📋 ดูสถานะระบบ")
            print("  2. 🔄 รัน Pipeline")
            print("  3. 📤 ส่งออกรายงาน")
            print("  4. 🔍 ดูข้อมูลแดชบอร์ด")
            print("  5. ❌ ออกจากระบบ")
            
            choice = input("\nเลือก: ").strip()
            
            if choice == "1":
                status = system.get_status()
                print(f"\n📋 สถานะระบบ: {status['status']}")
                print(f"⏱️  ทำงานมาแล้ว: {status['uptime_seconds']} วินาที")
                print("\n📊 สถานะแต่ละส่วน:")
                for name, active in status["systems"].items():
                    icon = "✅" if active else "❌"
                    print(f"   {icon} {name}")
            
            elif choice == "2":
                repo = input("URL Repository: ").strip()
                token = input("GitHub Token (ถ้ามี): ").strip() or None
                result = system.run_pipeline(repo, token)
                print(f"\nผลลัพธ์: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            elif choice == "3":
                fmt = input("รูปแบบ (excel/pdf): ").strip() or "excel"
                result = system.export_all_reports(fmt)
                print(f"\nผลลัพธ์: {result}")
            
            elif choice == "4":
                data = system.dashboard_data()
                print(f"\n📊 ข้อมูลแดชบอร์ด:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
            
            elif choice == "5":
                print("\n👋 ปิดระบบ...")
                break
    
    elif mode == "2":
        # โหมดรันเว็บเซิร์ฟเวอร์
        app, system = create_app()
        print("\n🌐 กำลังรันเว็บเซิร์ฟเวอร์ที่ http://localhost:5000")
        print("📊 แดชบอร์ดพร้อมใช้งานแล้ว\n")
        app.run(host='0.0.0.0', port=5000, debug=True)
    
    else:
        print("❌ เลือกไม่ถูกต้อง — ออกจากระบบ")
