import os
import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import subprocess
import sys


class FakeProducerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/apis'):
            payload = {"items": [{"id": "test-api-1", "name": "Test API"}]}
            body = json.dumps(payload).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()


def run_fake_producer(server):
    server.serve_forever()


def start_manager_process():
    # Start the FastAPI manager in a background process using the same Python interpreter
    return subprocess.Popen([sys.executable, '-m', 'uvicorn', 'apps.api_manager.manager:app', '--port', '8002'], cwd=os.getcwd())


def test_manager_sync_persists_catalog():
    # start fake producer
    server = HTTPServer(('127.0.0.1', 9001), FakeProducerHandler)
    t = threading.Thread(target=run_fake_producer, args=(server,), daemon=True)
    t.start()

    # start manager
    proc = start_manager_process()
    time.sleep(1.5)  # give uvicorn time to start

    try:
        url = 'http://127.0.0.1:8002/sync_from_producer'
        headers = {'X-Sync-Token': 'dev-sync-token'}
        resp = requests.post(url, json={'producer_url': 'http://127.0.0.1:9001'}, headers=headers, timeout=5)
        assert resp.status_code == 200

        # manager should have written data/manager_catalog.json
        catalog_path = os.path.join('data', 'manager_catalog.json')
        assert os.path.exists(catalog_path)
        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert 'test-api-1' in data
    finally:
        proc.terminate()
        server.shutdown()
        proc.wait(timeout=5)


if __name__ == '__main__':
    # allow running this file directly for a quick smoke-test
    test_manager_sync_persists_catalog()

