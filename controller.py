# controller.py
import yaml
from auth import env_for
from tasks import ensure_repo, build_if_any

with open("repos.yaml") as f:
    cfg = yaml.safe_load(f)

for r in cfg["repos"]:
    print(f"[RUN] {r['name']}")
    env = env_for(r["auth"])
    ensure_repo(r["name"], r["url"], r["branch"], env)
    if "build" in r.get("tasks", []):
        build_if_any(r["name"], env)

print("ALL DONE")
