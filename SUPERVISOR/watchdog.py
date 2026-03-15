import time
import requests
from pathlib import Path

ROOT = Path.home() / "MAKSIMAR_PLATFORM"
LOG = ROOT / "logs" / "system.log"

HEALTH_URL = "http://127.0.0.1:8000/health"
LATENCY_URL = "http://127.0.0.1:8000/health/latency"

CHECK_INTERVAL = 3
FAIL_LIMIT = 3


def log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[WATCHDOG] {ts} {msg}\n"

    with open(LOG, "a") as f:
        f.write(line)


def check_api():

    try:
        r = requests.get(HEALTH_URL, timeout=1)

        if r.status_code != 200:
            return False

        return True

    except Exception:
        return False


def main():

    fails = 0

    while True:

        ok = check_api()

        if ok:
            fails = 0

        else:
            fails += 1
            log(f"health check failed ({fails})")

            if fails >= FAIL_LIMIT:
                log("API unhealthy threshold reached")
                fails = 0

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
