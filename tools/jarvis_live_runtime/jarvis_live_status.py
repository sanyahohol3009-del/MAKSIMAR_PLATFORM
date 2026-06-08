from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any


RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
STATE_DIR = RUNTIME_ROOT / "state"
STATE_FILE = STATE_DIR / "jarvis_live_state.json"
HEARTBEAT_FILE = STATE_DIR / "jarvis_live_heartbeat.json"
PID_FILE = STATE_DIR / "jarvis_live.pid"


def main() -> int:
    status = build_status()
    print("JARVIS_LIVE_RUNTIME_STATUS")
    print(f"supervisor_running={str(status['supervisor_running']).lower()}")
    print(f"pid={status['pid']}")
    print(f"runtime_python={status['runtime_python']}")
    print(f"heartbeat_age_seconds={status['heartbeat_age_seconds']}")
    print(f"voice_loop_enabled={str(status['voice_loop_enabled']).lower()}")
    print("pc_control_allowed=false")
    print(f"latest_transcript={status['latest_transcript']}")
    print(f"latest_voice_reply={status['latest_voice_reply']}")
    return 0


def build_status() -> dict[str, Any]:
    state = _read_json(STATE_FILE)
    heartbeat = _read_json(HEARTBEAT_FILE)
    pid = _read_pid()
    heartbeat_updated_at = heartbeat.get("updated_at")
    heartbeat_age = None
    if isinstance(heartbeat_updated_at, int | float):
        heartbeat_age = round(time.time() - float(heartbeat_updated_at), 3)
    return {
        "supervisor_running": pid is not None and _process_alive(pid),
        "pid": pid or "",
        "runtime_python": str(state.get("runtime_python", "")),
        "heartbeat_age_seconds": heartbeat_age if heartbeat_age is not None else "",
        "voice_loop_enabled": bool(state.get("voice_loop_enabled", False)),
        "pc_control_allowed": False,
        "latest_transcript": str(state.get("latest_transcript", "")),
        "latest_voice_reply": str(state.get("latest_voice_reply", "")),
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if isinstance(payload, dict):
        return payload
    return {}


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


if __name__ == "__main__":
    raise SystemExit(main())
