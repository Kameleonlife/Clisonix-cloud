# -*- coding: utf-8 -*-
"""
asi_core_real.py – Real ASI Core (pa simulime, pa random)

Përfshin:
- ASICore: menaxhim i node-ve dhe logim real
- ClisonixNodeReal: raporton metrika reale të sistemit dhe ngarkon file audio/EEG
- ClisonixMeshNode: regjistron node-t te Mesh HQ dhe dërgon telemetry reale
"""

from __future__ import annotations
import json, datetime, time, socket, platform, os
from typing import Dict, Any

from asi_realtime_engine import ASIRealtimeEngine

try:
    import requests
except ImportError:
    requests = None

try:
    import psutil
except ImportError:
    psutil = None


class ASICore:
    """Bërthama reale e ASI – telemetri dhe status node-sh."""

    def __init__(
        self,
        hq_url: str = "http://localhost:7777/mesh/event",
        language: str = "sq",
    ) -> None:
        self.status = "active"
        self.hq_url = hq_url
        self.language = language
        self.nodes: Dict[str, Dict[str, Any]] = {
            "ALBA": {"status": "active", "role": "data_collector"},
            "ALBI": {"status": "active", "role": "neural_processor"},
            "JONA": {"status": "active", "role": "coordinator"},
        }
        self.logs: list[Dict[str, Any]] = []
        self.realtime_engine = ASIRealtimeEngine(log_dir="logs", language=language)
        self._recalculate_health()

    # ---------------- Language management ----------------
    def set_language(self, language: str) -> None:
        self.language = language
        self.realtime_engine.set_language(language)

    # ---------------- Logging & HQ transmission ----------------
    def log_event(self, source: str, event: str, level: str = "INFO") -> None:
        hints = {
            "ALBA": "Mbledhje e të dhënave dhe sinjaleve fizike.",
            "ALBI": "Analizë e sinjaleve dhe përpunim neural.",
            "JONA": "Koordinim i node-ve dhe sinkronizim i rrjetit."
        }
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "source": source,
            "event": event,
            "hint": hints.get(source, ""),
            "level": level,
        }
        self.logs.append(entry)
        print(f"[{source}] {level}: {event}")
        if entry["hint"]:
            print(f"💡 {entry['hint']}")
        self._send_to_hq(entry)

    def _send_to_hq(self, entry: Dict[str, Any]) -> None:
        if not requests:
            return
        try:
            requests.post(self.hq_url, json=entry, timeout=5)
        except Exception as exc:
            print(f"[ASI] ⚠️ HQ i paarritshëm: {exc}")

    # ---------------- Node health ----------------
    def update_node_status(self, node: str, status: str) -> None:
        if node not in self.nodes:
            self.log_event("ASI", f"Node i panjohur: {node}", "WARN")
            return
        self.nodes[node]["status"] = status
        self._recalculate_health()
        self.log_event(node, f"Statusi u përditësua në {status}")

    def _recalculate_health(self) -> None:
        active = sum(1 for n in self.nodes.values() if n["status"] == "active")
        self.health_score = round(active / len(self.nodes), 2)

    def analyze_status(self) -> Dict[str, Any]:
        print("📊 Analizë e gjendjes aktuale:")
        for name, info in self.nodes.items():
            st = info["status"]
            if st != "active":
                print(f"⚠️ {name}: {st} – kontrollo rrjetin ose energjinë.")
            else:
                print(f"✅ {name}: aktiv ({info['role']})")
        print(f"Shëndeti total: {self.health_score*100:.1f}%")
        return {
            "asi_status": self.status,
            "nodes": self.nodes,
            "health_score": self.health_score,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "realtime": self.realtime_engine.status(),
        }

    def export_logs(self, filename: str = "asi_logs.json") -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)
        print(f"[ASI] Loget u ruajtën në {filename}")

    def realtime_status(self) -> Dict[str, Any]:
        """Expose realtime engine status for external callers."""

        return self.realtime_engine.status()


class ClisonixNodeReal:
    """Node real që ngarkon file dhe raporton metrika të sistemit."""

    def __init__(self, asi_core: ASICore, node_id: str = "CLX-REAL") -> None:
        self.id = node_id
        self.asi = asi_core
        self.api_audio = "https://clisonix.com/api/uploads/audio/process"
        self.api_eeg = "https://clisonix.com/api/uploads/eeg/process"

    def collect_system_metrics(self) -> Dict[str, Any]:
        if not psutil:
            raise RuntimeError("psutil nuk është i instaluar – kërkohet për metrika reale.")
        net = psutil.net_io_counters()
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage(os.path.sep).percent,
            "net_sent_mb": round(net.bytes_sent / (1024 * 1024), 2),
            "net_recv_mb": round(net.bytes_recv / (1024 * 1024), 2),
            "timestamp": time.time(),
        }

    def transmit_audio_file(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            self.asi.log_event("ALBA", f"Audio file mungon: {filepath}", "WARN")
            return
        if not requests:
            self.asi.log_event("ALBA", "requests mungon – s'mund të ngarkohet audio", "ERROR")
            return
        with open(filepath, "rb") as f:
            res = requests.post(self.api_audio, files={"file": f}, timeout=10)
            self.asi.log_event("ALBA", f"Ngarkuar {os.path.basename(filepath)} → {res.status_code}")

    def transmit_eeg_file(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            self.asi.log_event("ALBI", f"EEG file mungon: {filepath}", "WARN")
            return
        if not requests:
            self.asi.log_event("ALBI", "requests mungon – s'mund të ngarkohet EEG", "ERROR")
            return
        with open(filepath, "rb") as f:
            res = requests.post(self.api_eeg, files={"file": f}, timeout=10)
            self.asi.log_event("ALBI", f"Ngarkuar EEG {os.path.basename(filepath)} → {res.status_code}")

    def report_system(self) -> None:
        metrics = self.collect_system_metrics()
        self.asi.log_event("ASI", f"Metrika reale: {metrics}")


class ClisonixMeshNode:
    """Node që lidhet me Mesh HQ dhe dërgon telemetry reale."""

    def __init__(self, asi_core: ASICore, node_id: str = "CLX-REAL", location: str = "Europe") -> None:
        self.asi = asi_core
        self.node_id = node_id
        self.location = location
        self.hq_url = "http://localhost:7777/mesh/register"
        self.status_url = "http://localhost:7777/mesh/status"
        self.hostname = socket.gethostname()
        try:
            self.ip = socket.gethostbyname(self.hostname)
        except Exception:
            self.ip = "127.0.0.1"
        self.status = "active"

    def collect_metrics(self) -> Dict[str, Any]:
        if not psutil:
            raise RuntimeError("psutil kërkohet për metrika reale.")
        net = psutil.net_io_counters()
        return {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage(os.path.sep).percent,
            "net_sent_mb": round(net.bytes_sent / (1024 * 1024), 2),
            "net_recv_mb": round(net.bytes_recv / (1024 * 1024), 2),
            "hostname": self.hostname,
            "ip": self.ip,
            "os": platform.system(),
            "version": platform.version(),
            "timestamp": time.time(),
        }

    def register_node(self) -> None:
        if not requests:
            self.asi.log_event("JONA", "requests mungon – s'mund të regjistrohet node", "ERROR")
            return
        payload = {
            "id": self.node_id,
            "location": self.location,
            "ip": self.ip,
            "hostname": self.hostname,
            "status": self.status,
        }
        res = requests.post(self.hq_url, json=payload, timeout=5)
        self.asi.log_event("JONA", f"Node i regjistruar në Mesh HQ → {res.status_code}")

    def send_status(self) -> None:
        if not requests:
            self.asi.log_event("ASI", "requests mungon – s'mund të dërgohet telemetry", "ERROR")
            return
        metrics = self.collect_metrics()
        payload = {"id": self.node_id, "status": self.status, "metrics": metrics}
        res = requests.post(self.status_url, json=payload, timeout=5)
        self.asi.log_event("ASI", f"Telemetry reale dërguar → {res.status_code}")


def _cli():
    import argparse
    parser = argparse.ArgumentParser(description="Run ASI Core në modalitet real")
    parser.add_argument("mode", choices=["node", "mesh"], help="node = Clisonix real, mesh = lidhje HQ")
    args = parser.parse_args()

    asi = ASICore()
    if args.mode == "node":
        node = ClisonixNodeReal(asi)
        node.report_system()
        node.transmit_audio_file("data/audio.wav")
        node.transmit_eeg_file("data/eeg.edf")
    elif args.mode == "mesh":
        mesh = ClisonixMeshNode(asi)
        mesh.register_node()
        mesh.send_status()


if __name__ == "__main__":
    _cli()
def get_system_status():
    return {
        "overall_health": "degraded",
        "active_nodes": 5,
        "total_nodes": 8,
        "last_checked": "just now",
        "issues": [
            {"node": "High-Frequency Audio Spectrometer", "issue": "Connection timeout"},
            {"node": "Industrial Vibration Sensors", "issue": "Scheduled maintenance"}
        ]
    }

