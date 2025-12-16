from pathlib import Path
import psutil, os, json, socket

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # rrënja e monorepo-s

COMMON_DIRS = ["backend", "frontend", "docs", "demo"]
SIG_FILES = {
    "backend": ["main.py", "server.py", "app.py", "requirements.txt"],
    "frontend": ["package.json", "next.config.js", "vite.config.ts", "astro.config.mjs"],
    "docs": ["mkdocs.yml", "docusaurus.config.js", "README.md"],
    "demo": ["package.json", "server.py", "app.py"]
}
COMMON_PORTS = [7777, 3000, 3001, 5173, 8080, 8000, 5555]

def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.25)
        try:
            s.connect(("127.0.0.1", port))
            return True
        except Exception:
            return False

def _guess_health(port: int):
    # kthe kombinime më tipike për health (FastAPI/Node)
    return [f"http://127.0.0.1:{port}/health",
            f"http://127.0.0.1:{port}/api/health",
            f"http://127.0.0.1:{port}/status"]

class SmartScanner:
    def scan_all(self):
        modules = []
        # 1) gjej direktori të rëndësishme
        for d in COMMON_DIRS:
            root = PROJECT_ROOT / d
            if not root.exists(): continue
            for sub in [root] + [p for p in root.iterdir() if p.is_dir()]:
                kind = self._classify(sub)
                if kind:
                    modules.append({"name": sub.name, "root": str(sub), "kind": kind})

        # 2) lista e porteve në përdorim nga procese reale
        listening = set()
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.status == psutil.CONN_LISTEN:
                listening.add(conn.laddr.port)

        # 3) për çdo modul, lidhe me një port të mundshëm dhe endpoint health
        enriched = []
        for m in modules:
            port = None
            # nëse një port tipik është “open”, lidhe
            for p in COMMON_PORTS:
                if _port_open(p):
                    port = p
                    break
            health_urls = _guess_health(port) if port else []
            enriched.append({**m, "port": port, "health_urls": health_urls})
        return enriched

    def _classify(self, path: Path):
        if not path.exists() or not path.is_dir(): return None
        files = {p.name for p in path.iterdir() if p.is_file()}
        for kind, sigs in SIG_FILES.items():
            if any(sf in files for sf in sigs):
                return kind
        return None

