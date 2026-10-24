#!/usr/bin/env python3
"""Independent OOB foundation monitor for MAKSIMAR."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Any

ROOT = Path.home() / "MAKSIMAR_PLATFORM"
RUNTIME_STATE_DIR = ROOT / "RUNTIME" / "state"
LOGS_DIR = ROOT / "logs"

RUNTIME_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "heartbeat_state.json"
GUARD_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "guard_heartbeat_state.json"
CORE_GUARD_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "core_guard_heartbeat_state.json"
KERNEL_HEARTBEAT_FILE = RUNTIME_STATE_DIR / "kernel_heartbeat_state.json"
PREFLIGHT_RESULT_FILE = RUNTIME_STATE_DIR / "preflight_result.json"

CONTROL_PLANE_HOST = "127.0.0.1"
CONTROL_PLANE_PORT = 8000
HEARTBEAT_FRESH_SEC = 10


def read_json(path: Path) -> dict[str, Any]:
    """Read JSON file if it exists."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def heartbeat_age_seconds(path: Path) -> float | None:
    """Return heartbeat age in seconds or None if unavailable."""
    payload = read_json(path)
    ts = payload.get("ts")
    if not isinstance(ts, (int, float)):
        return None
    return time.time() - float(ts)


def heartbeat_age(path: Path) -> str:
    """Return heartbeat age as human-readable string."""
    age = heartbeat_age_seconds(path)
    if age is None:
        return "missing"
    return f"{age:.2f}s"


def heartbeat_status(path: Path) -> str:
    """Return simplified heartbeat status."""
    payload = read_json(path)
    ts = payload.get("ts")
    if not isinstance(ts, (int, float)):
        return "MISSING"
    age = time.time() - float(ts)
    expected_source = {
        RUNTIME_HEARTBEAT_FILE: "process_supervisor",
        GUARD_HEARTBEAT_FILE: "stop_gate_watcher",
        CORE_GUARD_HEARTBEAT_FILE: "core_guard",
        KERNEL_HEARTBEAT_FILE: "kernel_watchdog",
    }.get(path)
    if age < -5 or payload.get("source") != expected_source:
        return "DEGRADED"
    if payload.get("status") != "alive":
        return "STOPPED" if payload.get("status") == "stopped" else "DEGRADED"
    if age <= HEARTBEAT_FRESH_SEC:
        return "ALIVE"
    return "STALE"


def runtime_truth_status() -> str:
    """Return aggregate runtime truth status."""
    hb = heartbeat_status(RUNTIME_HEARTBEAT_FILE)
    port = port_health()
    http = http_health()

    if hb == "ALIVE" and port == "LISTENING" and http == "ALIVE":
        return "UP"
    if hb == "MISSING" and port == "CLOSED" and http == "UNAVAILABLE":
        return "DOWN"
    if hb == "STALE":
        return "STALE"
    return "DEGRADED"


def port_health() -> str:
    """Return health of runtime port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    try:
        result = sock.connect_ex((CONTROL_PLANE_HOST, CONTROL_PLANE_PORT))
    finally:
        sock.close()

    return "LISTENING" if result == 0 else "CLOSED"


def http_health() -> str:
    """Return /health availability."""
    try:
        result = subprocess.run(
            [
                "curl",
                "-fsS",
                "--max-time",
                "2",
                f"http://{CONTROL_PLANE_HOST}:{CONTROL_PLANE_PORT}/health",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=3.0,
        )
    except Exception:
        return "UNAVAILABLE"

    return "ALIVE" if result.returncode == 0 else "UNAVAILABLE"


def tmux_status(session_name: str) -> str:
    """Return tmux session status."""
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        capture_output=True,
        text=True,
        check=False,
    )
    return "RUNNING" if result.returncode == 0 else "STOPPED"


def preflight_status() -> str:
    """Return preflight summary."""
    payload = read_json(PREFLIGHT_RESULT_FILE)
    if not payload:
        return "missing"
    return "ok=true" if payload.get("ok", False) else "ok=false"


def tail_log(path: Path, max_lines: int = 3) -> list[str]:
    """Read at most 64 KiB of the existing log; never load it for a small tail."""
    if max_lines <= 0:
        return []
    try:
        with path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            cursor = handle.tell()
            chunks: list[bytes] = []
            read_bytes = 0
            newline_count = 0
            while cursor > 0 and read_bytes < 65536 and newline_count <= max_lines:
                count = min(8192, cursor, 65536 - read_bytes)
                cursor -= count
                handle.seek(cursor)
                chunk = handle.read(count)
                chunks.insert(0, chunk)
                read_bytes += len(chunk)
                newline_count += chunk.count(b"\n")
            data = b"".join(chunks)
    except OSError:
        return []
    lines = data.decode("utf-8", errors="replace").splitlines()
    truncated = cursor > 0 and newline_count <= max_lines
    if cursor > 0 and newline_count:
        lines = lines[1:]  # The first suffix fragment is not a complete source line.
    lines = lines[-max_lines:]
    if truncated:
        marker = "[log tail truncated to 64 KiB; source retained] "
        lines = [marker + lines[0], *lines[1:]] if lines else [marker]
    return lines


def render_screen() -> str:
    """Build a plain-text OOB dashboard screen."""
    lines: list[str] = []
    lines.append("MAKSIMAR OOB FOUNDATION MONITOR")
    lines.append("=" * 80)
    lines.append(f"time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"preflight: {preflight_status()}")
    lines.append("")

    lines.append("SESSIONS")
    lines.append(f"  runtime: {tmux_status('maksimar')}")
    lines.append(f"  guard: {tmux_status('maksimar_guard')}")
    lines.append(f"  core_guard: {tmux_status('maksimar_core_guard')}")
    lines.append(f"  kernel_guard: {tmux_status('maksimar_kernel_guard')}")
    lines.append(f"  oob: {tmux_status('maksimar_oob')}")
    lines.append("")

    lines.append("RUNTIME TRUTH")
    lines.append(f"  runtime_truth: {runtime_truth_status()}")
    lines.append("")

    lines.append("HEARTBEATS")
    lines.append(f"  runtime_heartbeat: {heartbeat_status(RUNTIME_HEARTBEAT_FILE)} (age={heartbeat_age(RUNTIME_HEARTBEAT_FILE)})")
    lines.append(f"  guard_heartbeat: {heartbeat_status(GUARD_HEARTBEAT_FILE)} (age={heartbeat_age(GUARD_HEARTBEAT_FILE)})")
    lines.append(f"  core_guard_heartbeat: {heartbeat_status(CORE_GUARD_HEARTBEAT_FILE)} (age={heartbeat_age(CORE_GUARD_HEARTBEAT_FILE)})")
    lines.append(f"  kernel_heartbeat: {heartbeat_status(KERNEL_HEARTBEAT_FILE)} (age={heartbeat_age(KERNEL_HEARTBEAT_FILE)})")
    lines.append("")

    lines.append("RUNTIME ACCESS")
    lines.append(f"  port_8000: {port_health()}")
    lines.append(f"  /health: {http_health()}")
    lines.append("")

    lines.append("LOG TAILS")
    for name in ("system.log", "runtime.log", "guard.log", "core_guard.log", "kernel_guard.log"):
        lines.append(f"  --- {name} ---")
        tailed = tail_log(LOGS_DIR / name)
        if not tailed:
            lines.append("    <no lines>")
        else:
            for line in tailed:
                lines.append(f"    {line}")

    return "\n".join(lines)


def main() -> None:
    """Run independent OOB dashboard loop."""
    while True:
        os.system("clear")
        print(render_screen(), flush=True)
        time.sleep(2)


if __name__ == "__main__":
    main()
