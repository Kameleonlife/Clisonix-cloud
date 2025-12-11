#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clisonix Cloud â€” Launcher
- Start/stop/status for a set of services defined in Clisonix.yaml
- Rotating logs, PID tracking, health checks, graceful shutdown
- Windows-friendly (uses CREATE_NEW_PROCESS_GROUP, CTRL_BREAK_EVENT handling)

Usage:
  python launch_Clisonix_cloud.py init
  python launch_Clisonix_cloud.py up        [--timeout 120]
  python launch_Clisonix_cloud.py down      [--force]
  python launch_Clisonix_cloud.py restart
  python launch_Clisonix_cloud.py status
  python launch_Clisonix_cloud.py tail NAME

Requires:
  pip install pyyaml requests python-dotenv psutil
"""

import argparse
import os
import sys
import json
import time
import socket
import signal
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import yaml
    import requests
    from dotenv import load_dotenv
    import psutil
except Exception as e:
    print("[ERROR] Missing dependencies. Run:")
    print("  pip install pyyaml requests python-dotenv psutil")
    raise

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / ".Clisonix"
LOGS_DIR = ROOT / "logs"
PIDS_FILE = STATE_DIR / "pids.json"
CFG_FILE = ROOT / "Clisonix.yaml"
ENV_FILE = ROOT / ".env"

DEFAULT_CFG = """\
# Clisonix.yaml â€” service topology for Clisonix Cloud
# Edit paths/commands to match your environment.
version: 1
env:
  PYTHONUNBUFFERED: "1"
  LOG_LEVEL: "info"

services:
  - name: api
    cwd: "./services/api"
    cmd: ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8088"]
    log_file: "api.log"
    health:
      type: "http"
      url: "http://127.0.0.1:8088/health"
      timeout: 60

  - name: ingest
    cwd: "./services/ingest"
    cmd: ["python", "ingest.py"]
    log_file: "ingest.log"
    health:
      type: "tcp"
      host: "127.0.0.1"
      port: 8090
      timeout: 45

  - name: worker
    cwd: "./services/worker"
    cmd: ["python", "worker.py"]
    log_file: "worker.log"
    health:
      type: "none"

  - name: dashboard
    cwd: "./services/dashboard"
    cmd: ["npm", "run", "dev"]
    log_file: "dashboard.log"
    health:
      type: "http"
      url: "http://127.0.0.1:3002"
      timeout: 120
"""

DEFAULT_ENV = """\
# .env â€” environment for Clisonix Cloud
# Add secrets/keys here; they are loaded into the launcher process and inherited by services.
Clisonix_ENV=development
"""

def load_config():
    if not CFG_FILE.exists():
        print(f"[ERROR] Config not found: {CFG_FILE}")
        sys.exit(1)
    with CFG_FILE.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if "services" not in cfg or not isinstance(cfg["services"], list):
        print("[ERROR] Invalid config: missing 'services' list.")
        sys.exit(2)
    return cfg

def ensure_dirs():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def read_pids():
    if not PIDS_FILE.exists():
        return {}
    try:
        return json.loads(PIDS_FILE.read_text())
    except Exception:
        return {}

def write_pids(data):
    PIDS_FILE.write_text(json.dumps(data, indent=2))

def is_port_open(host: str, port: int, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def http_ok(url: str, timeout=2):
    try:
        r = requests.get(url, timeout=timeout)
        return 200 <= r.status_code < 400
    except Exception:
        return False

def check_health(svc, started_at):
    health = svc.get("health", {"type": "none"})
    typ = health.get("type", "none")
    timeout = int(health.get("timeout", 30))
    deadline = started_at + timeout
    name = svc["name"]

    if typ == "none":
        return True, "no-healthcheck"

    print(f"[{name}] healthcheck type={typ} timeout={timeout}s ...")
    while time.time() < deadline:
        if typ == "http":
            url = health["url"]
            if http_ok(url, timeout=3):
                return True, f"http OK: {url}"
        elif typ == "tcp":
            host = health["host"]
            port = int(health["port"])
            if is_port_open(host, port, timeout=2):
                return True, f"tcp OK: {host}:{port}"
        else:
            return True, "unknown health type -> skipping"
        time.sleep(1.5)
    return False, "timeout waiting for health"

def start_service(svc, env):
    name = svc["name"]
    cwd = (ROOT / svc.get("cwd", ".")).resolve()
    cmd = svc["cmd"]
    log_file = LOGS_DIR / svc.get("log_file", f"{name}.log")

    cwd.mkdir(parents=True, exist_ok=True)
    log_fp = open(log_file, "a", buffering=1, encoding="utf-8")

    creationflags = 0
    preexec_fn = None
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
    else:
        preexec_fn = os.setsid  # put in its own process group on POSIX

    print(f"[UP] {name}  cwd={cwd}  â†’ {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=log_fp,
        stderr=log_fp,
        env=env,
        creationflags=creationflags,
        preexec_fn=preexec_fn
    )
    return proc, log_fp, log_file

def stop_pid(pid, name, force=False):
    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print(f"[DOWN] {name}: already stopped")
        return True
    try:
        if os.name == "nt":
            if force:
                p.kill()
            else:
                p.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore[attr-defined]
                time.sleep(1.0)
                p.terminate()
        else:
            if force:
                p.kill()
            else:
                p.terminate()
        p.wait(timeout=15)
        print(f"[DOWN] {name}: stopped (pid={pid})")
        return True
    except Exception as e:
        print(f"[WARN] {name}: graceful stop failed: {e}; killing...")
        try:
            p.kill()
            p.wait(timeout=10)
            print(f"[DOWN] {name}: killed (pid={pid})")
            return True
        except Exception as e2:
            print(f"[ERROR] {name}: cannot kill pid={pid}: {e2}")
            return False

def cmd_init():
    ensure_dirs()
    if not CFG_FILE.exists():
        CFG_FILE.write_text(DEFAULT_CFG)
        print(f"[INIT] Created {CFG_FILE}")
    else:
        print(f"[INIT] {CFG_FILE} already exists")

    if not ENV_FILE.exists():
        ENV_FILE.write_text(DEFAULT_ENV)
        print(f"[INIT] Created {ENV_FILE}")
    else:
        print(f"[INIT] {ENV_FILE} already exists")

    print(f"[INIT] Logs: {LOGS_DIR}")
    print(f"[INIT] State: {STATE_DIR}")

def cmd_up(timeout):
    load_dotenv(ENV_FILE)  # load .env into process env
    cfg = load_config()
    ensure_dirs()

    # Merge envs: system â†’ cfg.env
    env = os.environ.copy()
    for k, v in (cfg.get("env") or {}).items():
        env.setdefault(k, str(v))

    pids = read_pids()
    any_running = False
    for name, meta in pids.items():
        if psutil.pid_exists(meta.get("pid", -1)):
            print(f"[WARN] service '{name}' seems running (pid={meta.get('pid')}); run 'down' first if needed.")
            any_running = True
    if any_running:
        print("[INFO] Continuing startup anywayâ€¦")

    started = {}
    for svc in cfg["services"]:
        proc, log_fp, log_path = start_service(svc, env)
        started[svc["name"]] = {
            "pid": proc.pid,
            "log": str(log_path),
            "started_at": int(time.time()),
        }
        ok, msg = check_health(svc, started[svc["name"]]["started_at"])
        status = "READY" if ok else "WAIT_TIMEOUT"
        print(f"[{svc['name']}] {status}: {msg}  (log: {log_path})")
        # keep log file handle open a bit in case next service depends on it
        log_fp.flush()
        # if you want to fail hard on health timeout, uncomment:
        # if not ok:
        #     print("[ERROR] Aborting startup due to health check failure.")
        #     break

    pids.update(started)
    write_pids(pids)
    print("[UP] All services launched (check `status` and `tail NAME`).")

def cmd_down(force=False):
    cfg = load_config() if CFG_FILE.exists() else {"services": []}
    pids = read_pids()
    if not pids:
        print("[DOWN] Nothing to stop.")
        return

    # stop in reverse order
    names = [s["name"] for s in cfg["services"]] if cfg.get("services") else list(pids.keys())
    for name in reversed(names):
        meta = pids.get(name)
        if not meta:
            continue
        pid = meta.get("pid")
        if pid:
            stop_pid(pid, name, force=force)
        pids.pop(name, None)
        write_pids(pids)
    print("[DOWN] Done.")

def cmd_status():
    cfg = load_config() if CFG_FILE.exists() else {"services": []}
    pids = read_pids()
    now = datetime.utcnow().isoformat() + "Z"
    print(f"[STATUS] {now}")
    names = [s["name"] for s in cfg["services"]] if cfg.get("services") else list(pids.keys())
    for name in names:
        meta = pids.get(name, {})
        pid = meta.get("pid")
        alive = psutil.pid_exists(pid) if pid else False
        log_path = meta.get("log", str(LOGS_DIR / f"{name}.log"))
        mark = "ðŸŸ¢" if alive else "ðŸ”´"
        print(f"  {mark} {name:12} pid={pid}  log={log_path}")

def cmd_tail(name):
    pids = read_pids()
    meta = pids.get(name)
    log_path = Path(meta["log"]) if meta and "log" in meta else LOGS_DIR / f"{name}.log"
    if not log_path.exists():
        print(f"[TAIL] No log file at {log_path}")
        return
    print(f"[TAIL] {log_path} (Ctrl+C to exit)")
    try:
        with log_path.open("r", encoding="utf-8", errors="ignore") as f:
            # seek to end
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.3)
                    continue
                sys.stdout.write(line)
                sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n[TAIL] Stopped.")

def cmd_restart():
    cmd_down(force=False)
    time.sleep(0.5)
    cmd_up(timeout=120)

def main():
    parser = argparse.ArgumentParser(description="Clisonix Cloud Launcher")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="scaffold config and env")

    up_p = sub.add_parser("up", help="start all services")
    up_p.add_argument("--timeout", type=int, default=120, help="overall start timeout (hint only)")

    down_p = sub.add_parser("down", help="stop all services")
    down_p.add_argument("--force", action="store_true", help="force kill")

    sub.add_parser("restart", help="restart all services")
    sub.add_parser("status", help="print service status")

    tail_p = sub.add_parser("tail", help="tail logs of a service")
    tail_p.add_argument("name", help="service name")

    args = parser.parse_args()

    # Ensure dirs
    ensure_dirs()

    if args.cmd == "init":
        cmd_init()
    elif args.cmd == "up":
        cmd_up(timeout=args.timeout)
    elif args.cmd == "down":
        cmd_down(force=args.force)
    elif args.cmd == "restart":
        cmd_restart()
    elif args.cmd == "status":
        cmd_status()
    elif args.cmd == "tail":
        cmd_tail(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
