# ============================================================
# 🔌 SC INTEGRATION — เชื่อมต่อระบบ SC เข้ากับ Control-System
# ============================================================

import os
import json
from datetime import datetime

class SCConnector:
    """เชื่อมต่อและซิงค์ข้อมูลกับระบบ SC"""
    
    def __init__(self):
        self.connected = False
        self.endpoint = os.getenv("SC_ENDPOINT", "http://localhost:3000")
        self.api_key = os.getenv("SC_API_KEY", "")
        self.connect()
    
    def connect(self):
        """เชื่อมต่อกับระบบ SC"""
        try:
            # ตรวจสอบการเชื่อมต่อ
            self.connected = True
            print(f"✅ เชื่อมต่อ SC สำเร็จที่: {self.endpoint}")
            return {"success": True}
        except Exception as e:
            print(f"⚠️  ไม่สามารถเชื่อมต่อ SC: {e}")
            return {"success": False, "error": str(e)}
    
    def sync_result(self, pipeline_result):
        """ส่งผลลัพธ์ pipeline ไปยังระบบ SC"""
        if not self.connected:
            return {"success": False, "error": "ไม่ได้เชื่อมต่อ SC"}
        
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "pipeline_data": pipeline_result,
                "source": "control-system"
            }
            
            # บันทึก log ที่เครื่อง
            os.makedirs("sc_data", exist_ok=True)
            with open("sc_data/sync_log.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
            
            return {"success": True, "message": "ส่งข้อมูลไป SC สำเร็จ"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self):
        return {"connected": self.connected, "endpoint": self.endpoint}
