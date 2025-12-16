import threading
import time
import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

# ----------------------------
# Real Producer Handler
# ----------------------------
class RealProducerHandler(BaseHTTPRequestHandler):
    """
    HTTP server që shërben të dhëna reale nga sistemet ASI / ALBA / ALBI / JONA
    në endpoint-in /apis. Nuk përdor mocke apo payload statikë.
    """

    def do_GET(self):
        if self.path.startswith('/apis'):
            try:
                # Marrim të dhënat reale nga Mesh HQ (p.sh. localhost:7777)
                mesh_url = "http://localhost:7777/status"
                res = requests.get(mesh_url, timeout=5)
                mesh_data = res.json() if res.status_code == 200 else {}

                # Përgatisim payload real për konsumatorin
                items = []
                trinity = mesh_data.get("trinity", {})
                for node, info in trinity.items():
                    items.append({
                        "id": node.lower(),
                        "name": node,
                        "role": info.get("role", "unknown"),
                        "status": info.get("status", "unknown"),
                        "health": info.get("health", 0),
                        "timestamp": mesh_data.get("timestamp")
                    })

                payload = {
                    "count": len(items),
                    "items": items
                }

                body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            except Exception as e:
                # Nëse ndodh një problem (p.sh. HQ offline)
                error = {"error": str(e)}
                body = json.dumps(error).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        else:
            self.send_response(404)
            self.end_headers()


# ----------------------------
# Run real producer server
# ----------------------------
def run_real_producer(port=9001):
    """
    Nis një server real që lexon të dhëna nga ASI Mesh HQ.
    """
    server = HTTPServer(('localhost', port), RealProducerHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"[REAL PRODUCER] Server running on port {port}")
    return server


# ----------------------------
# Sync me menaxherin real
# ----------------------------
def test_manager_sync():
    srv = run_real_producer(9001)
    try:
        # Dërgo kërkesë reale për sinkronizim te menaxheri
        payload = {"producer_url": "http://localhost:9001"}
        resp = requests.post('http://localhost:8002/sync_from_producer', json=payload, timeout=10)
        print("\n[MANAGER SYNC] Status:", resp.status_code)
        print("[MANAGER RESPONSE]:", resp.text)
    except Exception as e:
        print("\n[ERROR calling manager]:", e)
    finally:
        srv.shutdown()
        print("[REAL PRODUCER] Server stopped.")


if __name__ == '__main__':
    test_manager_sync()

