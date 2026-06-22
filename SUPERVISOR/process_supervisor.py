#!/usr/bin/env python3
"""MAKSIMAR runtime process supervisor."""

from __future__ import annotations

import os
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
    ensure_runtime_layout,
    resolve_canonical_python,
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


def build_environment() -> dict[str, str]:
    """Return environment for the Control Plane child process."""
    env = dict(os.environ)
    env.setdefault("JARVIS_HELPER_CLASSIFIER_ENABLED", "true")
    env.setdefault("JARVIS_HELPER_MODEL", "jarvis:helper3b")
    env.setdefault("OLLAMA_KEEP_ALIVE", "30m")
    env.setdefault("OLLAMA_NUM_PARALLEL", "1")
    env.setdefault("OLLAMA_MAX_LOADED_MODELS", "1")
    return env


def build_command() -> list[str]:
    """Return command for starting Control Plane with canonical interpreter."""
    python_path = resolve_canonical_python()
    return [
        str(python_path),
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

    try:
        canonical_python = resolve_canonical_python()
    except FileNotFoundError as exc:
        log(f"Missing canonical python: {exc}")
        sys.exit(1)

    if not canonical_python.exists():
        log(f"Canonical python does not exist: {canonical_python}")
        sys.exit(1)

    process: subprocess.Popen[str] | None = None
    stop_requested = False

    def handle_stop(signum: int, frame: object) -> None:
        """Handle termination signals."""
        del frame
        nonlocal stop_requested, process
        stop_requested = True
        log(f"Received stop signal: {signum}")
        if process and process.poll() is None:
            process.terminate()

    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    while not stop_requested:
        cmd = build_command()
        write_heartbeat("booting")
        log(f"Starting Control Plane: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            text=True,
            env=build_environment(),
        )

        while True:
            return_code = process.poll()
            if return_code is not None:
                break

            write_heartbeat("alive")
            time.sleep(POLL_INTERVAL_SEC)

        if stop_requested:
            write_heartbeat("stopped")
            log(f"Supervisor stopped. Child exit code: {return_code}")
            return

        write_heartbeat("broken")
        log(
            f"Control Plane exited with code {return_code}. "
            f"Restarting in {RESTART_DELAY_SEC}s..."
        )
        time.sleep(RESTART_DELAY_SEC)

    write_heartbeat("stopped")
    log("Supervisor exited cleanly.")


if __name__ == "__main__":
    main()
