#!/usr/bin/env python3
"""MAKSIMAR runtime process supervisor."""

from __future__ import annotations

import signal
import subprocess
import sys
import time

from CORE_ROOT.heartbeat_io import atomic_write_json, build_heartbeat
from CORE_ROOT.runtime_paths import (
    CONTROL_PLANE_HOST,
    CONTROL_PLANE_PORT,
    RUNTIME_HEARTBEAT_FILE,
    ROOT,
    SYSTEM_LOG_FILE,
    VENV_PYTHON,
    ensure_runtime_layout,
)

RESTART_DELAY_SEC = 2
POLL_INTERVAL_SEC = 2


def log(message: str) -> None:
    """Write a timestamped message to stdout and the shared system log."""
    ensure_runtime_layout()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[SUPERVISOR] {timestamp} {message}"
    print(line, flush=True)
    with SYSTEM_LOG_FILE.open("a", encoding="utf-8") as file_obj:
        file_obj.write(line + "\n")


def write_heartbeat(status: str = "alive") -> None:
    """Write runtime heartbeat atomically."""
    ensure_runtime_layout()
    payload = build_heartbeat(source="process_supervisor", status=status)
    atomic_write_json(RUNTIME_HEARTBEAT_FILE, payload)


def build_command() -> list[str]:
    """Return command for starting Control Plane with the venv interpreter."""
    return [
        str(VENV_PYTHON),
        "-m",
        "uvicorn",
        "CONTROL_PLANE.api_server:app",
        "--host",
        CONTROL_PLANE_HOST,
        "--port",
        str(CONTROL_PLANE_PORT),
    ]


def main() -> None:
    """Run supervisor loop and restart child if it exits unexpectedly."""
    ensure_runtime_layout()

    if not VENV_PYTHON.exists():
        log(f"Missing venv python: {VENV_PYTHON}")
        sys.exit(1)

    process: subprocess.Popen[str] | None = None
    stop_requested = False

    def handle_stop(signum: int, frame: object) -> None:
        nonlocal stop_requested, process
        stop_requested = True
        log(f"Received stop signal: {signum}")
        if process and process.poll() is None:
            process.terminate()

    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    while not stop_requested:
        write_heartbeat("alive")

        cmd = build_command()
        log(f"Starting Control Plane: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            text=True,
        )

        while True:
            write_heartbeat("alive")

            return_code = process.poll()
            if return_code is not None:
                break

            time.sleep(POLL_INTERVAL_SEC)

        if stop_requested:
            write_heartbeat("stopped")
            log(f"Supervisor stopped. Child exit code: {return_code}")
            return

        log(
            f"Control Plane exited with code {return_code}. "
            f"Restarting in {RESTART_DELAY_SEC}s..."
        )
        time.sleep(RESTART_DELAY_SEC)

    write_heartbeat("stopped")
    log("Supervisor exited cleanly.")


if __name__ == "__main__":
    main()
