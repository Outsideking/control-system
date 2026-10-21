# Placeholder controller
print("Controller ready")
# controller.py - ตัวสั่งการลูกข่าย
CLIENT_APPS = {
    "app1": "https://app-ลูก-1.vercel.app/api",
    "app2": "https://app-ลูก-2.vercel.app/api",
}

def send_command(app_name, action):
    # สั่งลูกข่ายได้จากตรงนี้
    print(f"สั่ง {app_name} ให้ทำ {action}")
    return {"status": "sent", "to": app_name, "action": action}

def broadcast(action):
    # สั่งพร้อมกันทุกตัว
    for app in CLIENT_APPS:
        send_command(app, action)
    return f"สั่ง {len(CLIENT_APPS)} แอพแล้ว: {action}"
# Outsideking - ScanzaClip Control System with Orc Protection
import os
import time
from datetime import datetime

# === ระบบทั้งหมดที่มี ===
ALL_SYSTEMS = {
    "orc": {"name": "Orc", "type": "AI Core", "source": "ScanzaClip", "permanent_off": False},
    "dashboard": {"name": "Dashboard", "type": "Web"},
    "control": {"name": "Control System", "type": "Main"},
    "api": {"name": "API Gateway", "type": "Service"},
    "pipelines": {"name": "Pipelines", "type": "Service"},
    # พ่อเพิ่มชื่อลูกข่ายตรงนี้ได้เรื่อยๆ
    # "app-luk-1": {"name": "App ลูก 1", "type": "Child"},
}

# สถานะเปิด/ปิด ชั่วคราว
SYSTEM_STATUS = {k: {"online": True, "off_until": None, "reason": ""} for k in ALL_SYSTEMS}

def log(action, system, detail=""):
    print(f"[{datetime.now()}] {action} -> {system} {detail}")
    return f"{action} {system}"

def control_system(name, action, reason="", duration=0):
    """
    สั่งเปิด/ปิดระบบด้วยชื่อ
    name = ชื่อระบบ เช่น orc, dashboard, api
    action = on / off / restart / status
    reason = เหตุผล
    duration = ปิดกี่นาที (0 = จนกว่าจะสั่งเปิด)
    
    ตัวอย่าง: control_system("dashboard", "off", "ซ่อมบำรุง", 30)
    """
    name = name.lower().strip()
    
    if name not in ALL_SYSTEMS:
        return {"error": f"ไม่เจอระบบชื่อ {name}", "available": list(ALL_SYSTEMS.keys())}
    
    sys_info = ALL_SYSTEMS[name]
    
    # === กฎเหล็กป้องกัน Orc ===
    if name == "orc":
        if action == "off" and duration == 0 and reason == "permanent":
            return {
                "status": "DENIED",
                "message": "⛔ ห้ามปิด Orc ถาวร! Orc เป็น AI กลางที่ใช้ทุกตัว",
                "rule": "Orc ปิดได้เฉพาะชั่วคราวตามต้องการเท่านั้น",
                "allow": "ใช้ off แบบระบุเวลา เช่น off 30 นาที"
            }
        # ปิดได้ แต่ต้องมีเวลาหรือเหตุผลชั่วคราว
        if action == "off":
            if duration == 0:
                duration = 10  # ถ้าไม่บอกเวลา ให้ปิดแค่ 10 นาทีแล้วเปิดเอง
    
    # === สั่งงาน ===
    if action == "off":
        SYSTEM_STATUS[name]["online"] = False
        SYSTEM_STATUS[name]["reason"] = reason
        if duration > 0:
            SYSTEM_STATUS[name]["off_until"] = time.time() + (duration * 60)
            msg = f"ปิด {name} ชั่วคราว {duration} นาที เหตุผล: {reason}"
        else:
            SYSTEM_STATUS[name]["off_until"] = None
            msg = f"ปิด {name} เหตุผล: {reason}"
        log("OFF", name, msg)
        return {"status": "OFF", "system": name, "message": msg, "auto_on_in": duration}
    
    elif action == "on":
        SYSTEM_STATUS[name]["online"] = True
        SYSTEM_STATUS[name]["off_until"] = None
        SYSTEM_STATUS[name]["reason"] = ""
        log("ON", name, "เปิดแล้ว")
        return {"status": "ON", "system": name, "message": f"เปิด {name} แล้ว"}
    
    elif action == "restart":
        SYSTEM_STATUS[name]["online"] = True
        log("RESTART", name, reason)
        return {"status": "RESTARTED", "system": name}
    
    elif action == "status":
        return {"system": name, "info": sys_info, "status": SYSTEM_STATUS[name]}

def check_auto_on():
    """เช็คตัวไหนหมดเวลาปิดชั่วคราว ให้เปิดเองอัตโนมัติ (โดยเฉพาะ Orc)"""
    now = time.time()
    for name, st in SYSTEM_STATUS.items():
        if not st["online"] and st["off_until"] and now > st["off_until"]:
            st["online"] = True
            st["off_until"] = None
            st["reason"] = ""
            log("AUTO-ON", name, "หมดเวลาปิดชั่วคราว เปิดเอง")

def status():
    check_auto_on()
    return {
        "all_systems": SYSTEM_STATUS,
        "orc_protected": True,
        "rule": "Orc ห้ามปิดถาวร ปิดได้เฉพาะตามต้องการเท่านั้น"
    }

def broadcast(action):
    """สั่งทุกตัว ยกเว้น Orc ถ้าเป็น off ถาวร"""
    results = {}
    for name in ALL_SYSTEMS:
        if name == "orc" and action == "off":
            results[name] = {"status": "SKIPPED", "reason": "Orc ป้องกันปิดถาวร"}
        else:
            results[name] = control_system(name, action)
    return results