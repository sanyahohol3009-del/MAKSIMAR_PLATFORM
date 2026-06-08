from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME" / "jarvis_live"
STATE_DIR = RUNTIME_ROOT / "state"
LOG_DIR = RUNTIME_ROOT / "logs"
STATE_FILE = STATE_DIR / "jarvis_live_state.json"
HEARTBEAT_FILE = STATE_DIR / "jarvis_live_heartbeat.json"
PID_FILE = STATE_DIR / "jarvis_live.pid"
EVENT_LOG_FILE = LOG_DIR / "jarvis_live_events.jsonl"
BACKGROUND_LOOP = (
    Path(__file__).resolve().parent / "jarvis_live_background_loop.py"
)
FASTER_WHISPER_RUNTIME_PYTHON = (
    Path.home() / "MAKSIMAR_RUNTIME" / "venvs" / "faster_whisper_stt" / "bin" / "python"
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--background", action="store_true")
    args = parser.parse_args(argv)
    _ensure_runtime_dirs()
    runtime_python = _runtime_python()

    current_pid = _read_pid()
    if current_pid is not None and _process_alive(current_pid):
        _write_state(
            "running",
            current_pid,
            "duplicate_start_refused",
            runtime_python=runtime_python,
        )
        print(f"JARVIS Live: already running pid={current_pid}")
        print(f"runtime_python={runtime_python}")
        return 0

    process = subprocess.Popen(  # noqa: S603 - controlled self-start only.
        [runtime_python, str(BACKGROUND_LOOP)],
        cwd=str(Path.cwd()),
        start_new_session=True,
        stdout=subprocess.DEVNULL if args.background else None,
        stderr=subprocess.DEVNULL if args.background else None,
    )
    PID_FILE.write_text(str(process.pid), encoding="utf-8")
    _write_state(
        "starting",
        process.pid,
        "background_supervisor_started",
        runtime_python=runtime_python,
    )
    _append_event({"event": "start", "pid": process.pid, "runtime_python": runtime_python})
    print(f"JARVIS Live: starting pid={process.pid}")
    print(f"runtime_python={runtime_python}")
    print(f"state_file={STATE_FILE}")
    return 0


def _runtime_python() -> str:
    env_python = os.environ.get("JARVIS_LIVE_RUNTIME_PYTHON", "").strip()
    if env_python and _is_executable(Path(env_python).expanduser()):
        return str(Path(env_python).expanduser())
    if _is_executable(FASTER_WHISPER_RUNTIME_PYTHON):
        return str(FASTER_WHISPER_RUNTIME_PYTHON)
    return sys.executable


def _is_executable(path: Path) -> bool:
    return path.exists() and path.is_file() and os.access(path, os.X_OK)


def _ensure_runtime_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


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


def _write_state(
    state: str,
    pid: int | None,
    reason: str,
    runtime_python: str,
) -> None:
    payload = {
        "state": state,
        "pid": pid,
        "reason": reason,
        "runtime_python": runtime_python,
        "updated_at": time.time(),
        "voice_loop_enabled": True,
        "pc_control_allowed": False,
        "latest_transcript": "",
        "latest_voice_reply": "",
    }
    STATE_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )


def _append_event(payload: dict[str, Any]) -> None:
    payload = {"updated_at": time.time(), **payload, "pc_control_allowed": False}
    with EVENT_LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
