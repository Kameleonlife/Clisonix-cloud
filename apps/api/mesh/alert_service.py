import os
import requests

WEBHOOK = os.getenv("MESH_ALERT_WEBHOOK")

THRESH = {
    "cpu": 90,
    "mem": 90,
    "disk": 95,
}

def evaluate(rec: dict):
    alerts = []
    m = rec.get("metrics", {})
    if m.get("cpu", 0) > THRESH["cpu"]:
        alerts.append("high_cpu")
    if m.get("mem", 0) > THRESH["mem"]:
        alerts.append("high_mem")
    if m.get("disk", 0) > THRESH["disk"]:
        alerts.append("high_disk")
    return alerts

def notify(rec: dict, alerts: list):
    if not WEBHOOK:
        return False
    payload = {"node": rec.get("id"), "alerts": alerts, "metrics": rec.get("metrics", {})}
    try:
        r = requests.post(WEBHOOK, json=payload, timeout=3)
        return r.status_code >= 200 and r.status_code < 300
    except Exception:
        return False
