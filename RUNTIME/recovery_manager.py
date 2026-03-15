#!/usr/bin/env python3
import json
import time
from pathlib import Path

ROOT = Path.home() / "MAKSIMAR_PLATFORM"

HEARTBEAT_FILE = ROOT / "CORE_ROOT" / "heartbeat_state.json"
GUARD_HEARTBEAT_FILE = ROOT / "CORE_ROOT" / "guard_heartbeat_state.json"
DEGRADED_FLAG = ROOT / "RUNTIME" / "degraded_mode.flag"
LAST_REASON_FILE = ROOT / "RUNTIME" / "last_degraded_reason.txt"
LOG_FILE = ROOT / "logs" / "system.log"

HEARTBEAT_TIMEOUT = 10
GUARD_TIMEOUT = 12


def log(message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[RECOVERY] {timestamp} {message}"
    print(line, flush=True)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def heartbeat_alive(payload: dict, timeout: int) -> tuple[bool, str]:
    source = payload.get("source", "unknown")
    status = payload.get("status", "unknown")
    ts = float(payload.get("ts", 0))

    age = time.time() - ts

    if status != "alive":
        return False, f"status={status}, source={source}"

    if age > timeout:
        return False, f"timeout age={age:.2f}s, source={source}, limit={timeout}s"

    return True, f"alive age={age:.2f}s, source={source}"


def clear_degraded_state() -> None:
    if DEGRADED_FLAG.exists():
        DEGRADED_FLAG.unlink()
        log("Removed stale degraded_mode.flag")

    else:
        log("No degraded_mode.flag to remove")


def main() -> None:
    try:
        runtime_payload = load_json(HEARTBEAT_FILE)
        guard_payload = load_json(GUARD_HEARTBEAT_FILE)

        runtime_ok, runtime_msg = heartbeat_alive(runtime_payload, HEARTBEAT_TIMEOUT)
        guard_ok, guard_msg = heartbeat_alive(guard_payload, GUARD_TIMEOUT)

        if runtime_ok and guard_ok:
            clear_degraded_state()
            log(f"Recovery OK: runtime={runtime_msg}; guard={guard_msg}")
            return

        log(f"Recovery skipped: runtime={runtime_msg}; guard={guard_msg}")

        if LAST_REASON_FILE.exists():
            log(f"Last degraded reason preserved in {LAST_REASON_FILE}")

    except Exception as exc:
        log(f"Recovery manager failed: {exc}")


if __name__ == "__main__":
    main()
