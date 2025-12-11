import time

from services.asi_system import ASISystem


def test_asi_system_start_stop():
    sys = ASISystem(name="test-asi")
    assert sys.health_check()["status"] == "stopped"
    sys.start()
    h = sys.health_check()
    assert h["status"] == "running"
    assert h["name"] == "test-asi"
    assert h["uptime_seconds"] >= 0
    # ensure uptime increases
    time.sleep(0.02)
    assert sys.health_check()["uptime_seconds"] >= h["uptime_seconds"]
    sys.stop()
    assert sys.health_check()["status"] == "stopped"
