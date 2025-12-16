class SandboxCore:
    """Sandbox Monitoring Core"""
    def __init__(self):
        self.status = "active"
    def log_event(self, event: str):
        print(f"[SANDBOX] Event: {event}")

