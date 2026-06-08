from __future__ import annotations

import json
import os
import signal
import time
from pathlib import Path


RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
STATE_DIR = RUNTIME_ROOT / "state"
LOG_DIR = RUNTIME_ROOT / "logs"
STATE_FILE = STATE_DIR / "jarvis_live_state.json"
PID_FILE = STATE_DIR / "jarvis_live.pid"
EVENT_LOG_FILE = LOG_DIR / "jarvis_live_events.jsonl"


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    pid = _read_pid()
    if pid is None:
        _write_state("stopped", None, "no_pid_file")
        print("JARVIS Live: stopped")
        return 0
    if _process_alive(pid):
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.2)
    _write_state("stopped", pid, "explicit_stop_command")
    PID_FILE.unlink(missing_ok=True)
    _append_event({"event": "stop", "pid": pid})
    print(f"JARVIS Live: stopped pid={pid}")
    return 0


def _read_pid() -> int | None:
    if not PID_FILE.exists():
        return None
    value = PID_FILE.read_text(encoding="utf-8").strip()
    if not value.isdigit():
        return None
    return int(value)


def _process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _write_state(state: str, pid: int | None, reason: str) -> None:
    payload = {
        "state": state,
        "pid": pid,
        "reason": reason,
        "updated_at": time.time(),
        "voice_loop_enabled": False,
        "pc_control_allowed": False,
        "latest_transcript": "",
        "latest_voice_reply": "",
    }
    STATE_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )


def _append_event(payload: dict[str, object]) -> None:
    payload = {"updated_at": time.time(), **payload, "pc_control_allowed": False}
    with EVENT_LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
