import time, requests, psutil, json

def _get(url: str, timeout=1.5):
    try:
        r = requests.get(url, timeout=timeout)
        ok = r.status_code < 500
        data = None
        fmt = None
        # provoj JSON ose CBOR (nëse kthen content-type të tillë)
        ct = r.headers.get("content-type","")
        if "application/json" in ct:
            data = r.json(); fmt = "json"
        elif "application/cbor" in ct:
            try:
                import cbor2
                data = cbor2.loads(r.content); fmt = "cbor"
            except Exception:
                data = None; fmt = "binary"
        return {"ok": ok, "status": r.status_code, "data": data, "format": fmt}
    except Exception as e:
        return {"ok": False, "status": None, "err": str(e)}

def _latency(url: str, timeout=1.5):
    t0 = time.time()
    try:
        requests.get(url, timeout=timeout)
        return round((time.time()-t0)*1000, 2)
    except Exception:
        return None

class AutoMonitor:
    def observe(self, modules: list[dict], duration_sec: int = 10):
        """
        Vëzhgon module reale për ~duration_sec:
        - nëse ka /health, e thërret, lexon JSON/CBOR
        - mat CPU/RAM të sistemit (si proxy—për proces specifik kërkon integrim me pid mapping)
        - mat latency tek endpoint i parë i gjetur
        """
        start = time.time()
        out = []
        while time.time() - start < duration_sec:
            # matjet përditësohen çdo 2 sekonda
            snap = []
            for m in modules:
                metrics = {
                    "cpu": psutil.cpu_percent(interval=None),
                    "ram": psutil.virtual_memory().percent,
                }
                health = {"ok": False, "status": None}
                intel = {"format": None}
                latency_ms = None
                if m.get("health_urls"):
                    url = m["health_urls"][0]
                    h = _get(url)
                    health = {"ok": h["ok"], "status": h.get("status")}
                    intel = {"format": h.get("format")}
                    latency_ms = _latency(url)

                record = {
                    **m,
                    "metrics": {**metrics, "latency_ms": latency_ms},
                    "health": health,
                    "intel": intel,
                    "updated": time.time()
                }
                snap.append(record)
            out = snap
            time.sleep(2)

        return out

