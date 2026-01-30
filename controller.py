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
import os
import subprocess
import sys

PYTHON37 = os.path.join(os.getcwd(), "venv37_x64", "bin", "python")  # Linux/Mac
# PYTHON37 = os.path.join(os.getcwd(), "venv37_x64", "Scripts", "python.exe")  # Windows

def run_pipeline_version(repo_name, version="3.7"):
    if version=="3.7":
        cmd = [PYTHON37, "simulate_run.py"]
    else:
        cmd = [sys.executable, "simulate_run.py"]  # default env
    print(f"Running {repo_name} with Python {version}...")
    subprocess.run(cmd)

# Example usage
run_pipeline_version("myrepo1", version="3.7")
run_pipeline_version("myrepo2")  # default python
