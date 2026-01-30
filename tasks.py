# tasks.py
import subprocess, os

def sh(cmd, env=None):
    subprocess.check_call(cmd, shell=True, env=env)

def ensure_repo(name, url, branch, env):
    if not os.path.isdir(name):
        sh(f"git clone {url} {name}", env)
    sh(f"cd {name} && git checkout {branch} && git pull", env)

def build_if_any(name, env):
    if os.path.isfile(f"{name}/Makefile"):
        sh(f"cd {name} && make", env)
    elif os.path.isfile(f"{name}/package.json"):
        sh(f"cd {name} && npm install && npm run build", env)
    elif os.path.isfile(f"{name}/pyproject.toml"):
        sh(f"cd {name} && pip install -e .", env)
