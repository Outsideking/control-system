# ============================================================
# 🔌 SCANZACLIP INTEGRATION — เชื่อมต่อระบบ ScanZaclip
# ============================================================

import os
import json
from datetime import datetime

class ScanZaclip:
    """ระบบบันทึกและวิเคราะห์ข้อมูลสำหรับ ScanZaclip"""
    
    def __init__(self):
        self.log_dir = "scanzaclip_logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "data_log.jsonl")
        print("✅ ScanZaclip พร้อมใช้งาน")
    
    def log_data(self, data):
        """บันทึกข้อมูลจาก pipeline"""
        try:
            entry = {
                "time": datetime.now().isoformat(),
                "type": "pipeline_result",
                "data": data
            }
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
            return {"success": True, "log_entry": entry}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_recent_logs(self, limit=10):
        """อ่านข้อมูลล่าสุด"""
        if not os.path.exists(self.log_file):
            return []
        
        lines = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(json.loads(line))
                if len(lines) >= limit:
                    break
        
        return list(reversed(lines))
