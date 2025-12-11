import time
import requests

def rtt_http(url: str, timeout: float = 2.0):
    """Return round-trip time in milliseconds for a simple GET, or None on failure."""
    try:
        start = time.time()
        r = requests.get(url, timeout=timeout)
        if r.status_code >= 200 and r.status_code < 400:
            return int((time.time() - start) * 1000)
    except Exception:
        return None
    return None
