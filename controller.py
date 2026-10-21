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