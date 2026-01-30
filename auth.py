# auth.py
import os

def env_for(auth):
    env = os.environ.copy()
    if auth == "token":
        token = env.get("GITHUB_TOKEN")
        if not token:
            raise RuntimeError("GITHUB_TOKEN not set")
        env["GIT_HTTP_EXTRAHEADER"] = f"Authorization: Bearer {token}"
    return env
