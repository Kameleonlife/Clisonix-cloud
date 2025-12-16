import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
from backend.system.email_reporter import send_daily_report

TZ = ZoneInfo("Europe/Berlin")
RUN_HOUR = 8
RUN_MIN  = 0

def next_run_dt(now=None):
    now = now or datetime.now(TZ)
    run = now.replace(hour=RUN_HOUR, minute=RUN_MIN, second=0, microsecond=0)
    if run <= now:
        run = run + timedelta(days=1)
    return run

def main_loop():
    while True:
        target = next_run_dt()
        sleep_sec = (target - datetime.now(TZ)).total_seconds()
        if sleep_sec > 0:
            time.sleep(sleep_sec)
        try:
            pdf_path = send_daily_report()
            print(f"[Scheduler] Sent daily report: {pdf_path}")
        except Exception as e:
            print(f"[Scheduler] ERROR sending report: {e}")
        # schedule next shortly
        time.sleep(1)

if __name__ == "__main__":
    print("[Scheduler] Daily email at 08:00 Europe/Berlin. Running…")
    main_loop()

