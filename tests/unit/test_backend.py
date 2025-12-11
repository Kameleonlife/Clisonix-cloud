import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_asi_status():
    response = client.get("/asi/status")
    assert response.status_code == 200
    data = response.json()
    assert "trinity" in data
    assert "alba" in data["trinity"]
    assert "albi" in data["trinity"]
    assert "jona" in data["trinity"]

def test_error_handling():
    # Endpoint që nuk ekziston
    response = client.get("/notfound")
    assert response.status_code == 404
