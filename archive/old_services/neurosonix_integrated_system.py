# -*- coding: utf-8 -*-
"""
Clisonix Integrated System â€” with Distributed Pulse Balancer Integration
Industrial-Grade Real-Time Integration + Cloud Upload + Cluster-Aware Routing

Business: Ledjan Ahmati - WEB8euroweb GmbH
REAL DATA ONLY â€¢ NO MOCK â€¢ NO RANDOM â€¢ NO PLACEHOLDER
"""

import os
import json
import os
import time
import uuid
from datetime import datetime
from pathlib import Path

import platform
import psutil
import requests

from Clisonix.colored_logger import setup_logger
BASE_DIR = Path(r"C:\Clisonix-cloud")
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

SYSTEM_ID = f"Clisonix-{platform.node()}"

# Upload lokal (zakonisht API FastAPI vendase)
DEFAULT_API_ENDPOINT = os.getenv("NSX_API_ENDPOINT", "http://localhost:8080/metrics/upload")

# Balancer endpoint (ndrysho nÃ«se Ã«shtÃ« nÃ« node tjetÃ«r)
BALANCER_API = os.getenv("NSX_BALANCER_API", "http://localhost:8091/balancer/request")

# Intervali i ciklit
UPLOAD_INTERVAL = int(os.getenv("NSX_UPLOAD_INTERVAL", "15"))

# Opsionale: API KEY (nÃ«se backend kÃ«rkon autentikim)
API_KEY = os.getenv("NSX_API_KEY", "").strip()

REALTIME_FILE = LOG_DIR / "system_metrics.jsonl"
SENSOR_LOG   = LOG_DIR / "sensor_stream.jsonl"
ERROR_LOG    = LOG_DIR / "errors.log"

SESSION = requests.Session()
DEFAULT_TIMEOUT = (3, 7)  # (connect, read) seconds

logger = setup_logger("ClisonixIntegrated")

# =====================================================
# ðŸ§  DATA COLLECTION
# =====================================================
def collect_system_metrics() -> dict:
    """Mbledh metrika reale nga sistemi."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system_id": SYSTEM_ID,
        "node": platform.node(),
        "os": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "net_io_sent_MB": round(psutil.net_io_counters().bytes_sent / (1024**2), 2),
        "net_io_recv_MB": round(psutil.net_io_counters().bytes_recv / (1024**2), 2),
        "active_processes": len(psutil.pids()),
        "uptime_sec": round(time.time() - psutil.boot_time())
    }

def collect_sensor_data() -> dict:
    """Lexon tÃ« dhÃ«na reale nga sensorÃ«t e disponueshÃ«m nÃ« host (temp, bateri)."""
    # Temperatura CPU (nÃ«se suportuar nga OS/driver-at)
    temperature = None
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if temps:
            # Merr elementin e parÃ« tÃ« sensorit tÃ« parÃ« si â€œpÃ«rfaqÃ«suesâ€
            for name, entries in temps.items():
                if entries:
                    temperature = round(entries[0].current, 2)
                    break

    # Bateria (nÃ«se ekziston; p.sh. nÃ« laptop)
    battery = None
    if hasattr(psutil, "sensors_battery"):
        bat = psutil.sensors_battery()
        if bat:
            battery = bat.percent

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "device": "ALBA AI Temperature Control",
        "temperature_C": temperature,
        "battery_percent": battery,
        "status": "active"
    }

# =====================================================
# ðŸ’¾ STORAGE HELPERS
# =====================================================
def append_jsonl(file_path: Path, data: dict):
    """Shton njÃ« rekord JSONL nÃ« disk."""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def log_error(msg: str):
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {msg}\n")

# =====================================================
# ðŸŒ NETWORK HELPERS
# =====================================================
def headers():
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["Authorization"] = f"Bearer {API_KEY}"
    return h

def upload_to_endpoint(endpoint: str, payload: dict) -> bool:
    """DÃ«rgon payload nÃ« endpoint-in e dhÃ«nÃ«. Kthen True nÃ« sukses."""
    try:
        r = SESSION.post(endpoint, json=payload, headers=headers(), timeout=DEFAULT_TIMEOUT)
        if r.status_code == 200:
            logger.info("Upload OK -> %s", endpoint)
            return True
        else:
            logger.warning(
                "Upload failed [%s] -> %s | %s",
                r.status_code,
                endpoint,
                r.text[:200],
            )
            log_error(f"UPLOAD_FAIL {r.status_code} {endpoint} {r.text[:500]}")
            return False
    except Exception as e:
        logger.error("Upload error -> %s | %s", endpoint, e)
        log_error(f"UPLOAD_ERROR {endpoint} {e}")
        return False

def ask_balancer_for_target(work_id: str, weight: float = 1.0) -> dict | None:
    """Pyet Balancer-in pÃ«r vendim rishpÃ«rndarjeje."""
    body = {"work_id": work_id, "weight": float(weight)}
    try:
        r = SESSION.post(BALANCER_API, json=body, headers=headers(), timeout=DEFAULT_TIMEOUT)
        if r.status_code != 200:
            logger.warning("Balancer HTTP %s", r.status_code)
            log_error(f"BALANCER_HTTP_{r.status_code} {r.text[:300]}")
            return None
        return r.json()
    except Exception as e:
        logger.error("Balancer unreachable: %s", e)
        log_error(f"BALANCER_UNREACHABLE {e}")
        return None

# =====================================================
# ðŸ” MAIN LOOP
# =====================================================
def decide_and_dispatch(combined: dict):
    """
    Vendos si tÃ« dÃ«rgohet pulsi duke pyetur balancer-in.
    Fallback: dÃ«rgo te DEFAULT_API_ENDPOINT nÃ«se balancer nuk pÃ«rgjigjet.
    """
    work_id = combined.get("system", {}).get("system_id") or f"work-{uuid.uuid4()}"
    decision = ask_balancer_for_target(work_id=work_id)

    if not decision:
        # Balancer offline â†’ dÃ«rgo lokalisht te endpoint default
        logger.info("Balancer offline -> local upload fallback")
        upload_to_endpoint(DEFAULT_API_ENDPOINT, combined)
        return

    dec_type = decision.get("decision")
    target_api = decision.get("target")
    leader_api = decision.get("leader_api")

    if dec_type == "accepted_local":
        logger.info("Accepted local by node -> uploading locally")
        upload_to_endpoint(DEFAULT_API_ENDPOINT, combined)
    elif dec_type == "redirect" and target_api:
        logger.info("Redirect by leader -> %s", target_api)
        # DÃ«rgo te target node (presa qÃ« target tÃ« ketÃ« /metrics/upload)
        ok = upload_to_endpoint(target_api.rstrip("/") + "/metrics/upload", combined)
        if not ok:
            # nÃ«se dÃ«shtoi redirect â†’ fallback lokal
            logger.warning("Redirect failed -> fallback to local endpoint")
            upload_to_endpoint(DEFAULT_API_ENDPOINT, combined)
    elif dec_type == "redirect_to_leader" and leader_api:
        logger.info("Redirect to leader -> %s", leader_api)
        ok = upload_to_endpoint(leader_api.rstrip("/") + "/metrics/upload", combined)
        if not ok:
            logger.warning("Leader upload failed -> fallback to local endpoint")
            upload_to_endpoint(DEFAULT_API_ENDPOINT, combined)
    else:
        # Rast i panjohur â†’ fallback lokal
        logger.info("Unknown decision -> local upload")
        upload_to_endpoint(DEFAULT_API_ENDPOINT, combined)

def monitor_loop():
    logger.info(
        "Clisonix Integrated System (Cluster-Aware) â€” Node: %s",
        platform.node(),
    )
    logger.info("Default API: %s", DEFAULT_API_ENDPOINT)
    logger.info("Balancer API: %s", BALANCER_API)
    logger.info("Interval: %ss | Logs: %s", UPLOAD_INTERVAL, LOG_DIR)

    while True:
        # 1) Mbledh tÃ« dhÃ«nat reale
        sys_metrics = collect_system_metrics()
        sensor_data = collect_sensor_data()

        # 2) Ruaj backup lokal
        append_jsonl(REALTIME_FILE, sys_metrics)
        append_jsonl(SENSOR_LOG, sensor_data)

        # 3) PÃ«rgatit payload-in e pÃ«rbashkÃ«t
        combined = {
            "timestamp": datetime.utcnow().isoformat(),
            "system": sys_metrics,
            "sensor": sensor_data,
            "version": "3.1.0-cluster"
        }

        # 4) Vendos dhe dÃ«rgo (me balancer + fallback)
        decide_and_dispatch(combined)

        # 5) Print status i shkurtÃ«r nÃ« console
        logger.debug(
            "CPU %.1f%% | MEM %.1f%% | TEMP %sÂ°C",
            sys_metrics["cpu_percent"],
            sys_metrics["memory_percent"],
            sensor_data.get("temperature_C"),
        )
        time.sleep(UPLOAD_INTERVAL)

# =====================================================
# â–¶ï¸ ENTRY POINT
# =====================================================
if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logger.info("Monitoring stopped manually")
    except Exception as e:
        log_error(f"FATAL {e}")
        logger.critical("Critical error logged: %s", e)

