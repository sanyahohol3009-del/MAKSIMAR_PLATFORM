#!/usr/bin/env python3
"""MAKSIMAR core guard."""

from __future__ import annotations

import subprocess
import time

from CORE_ROOT.heartbeat_io import (
    atomic_write_json,
    build_heartbeat,
    heartbeat_age_seconds,
    heartbeat_source,
    heartbeat_status,
    safe_read_json,
)
from CORE_ROOT.runtime_paths import (
    CORE_GUARD_HEARTBEAT_FILE,
    CORE_GUARD_LOG_FILE,
    GUARD_HEARTBEAT_FILE,
    GUARD_SESSION_NAME,
    STOP_GATE_SCRIPT,
    SYSTEM_LOG_FILE,
    ensure_runtime_layout,
)

HEARTBEAT_TIMEOUT_SEC = 12.0
POLL_INTERVAL_SEC = 2.0
SOURCE_READY_GRACE_SEC = 8.0
SOURCE_MISMATCH_STRIKE_LIMIT = 3


def log(message: str) -> None:
    """Write a core guard log line."""
    ensure_runtime_layout()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[CORE-GUARD] {timestamp} {message}"
    print(line, flush=True)

    for log_file in (CORE_GUARD_LOG_FILE, SYSTEM_LOG_FILE):
        with log_file.open("a", encoding="utf-8") as file_obj:
            file_obj.write(line + "\n")


def tmux_session_exists(session_name: str) -> bool:
    """Return True if tmux session exists."""
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def process_exists(pattern: str) -> bool:
    """Return True if a process matching pattern exists."""
    result = subprocess.run(
        ["pgrep", "-f", pattern],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def write_self_heartbeat(status: str = "alive") -> None:
    """Write the core guard heartbeat."""
    ensure_runtime_layout()
    payload = build_heartbeat(source="core_guard", status=status)
    atomic_write_json(CORE_GUARD_HEARTBEAT_FILE, payload)


def evaluate_guard(
    started_at: float,
    source_mismatch_strikes: int,
) -> tuple[bool, str, int]:
    """Evaluate stop-gate watcher heartbeat."""
    payload = safe_read_json(GUARD_HEARTBEAT_FILE)
    if payload is None:
        return (
            False,
            f"guard heartbeat not ready yet: {GUARD_HEARTBEAT_FILE}",
            0,
        )

    source = heartbeat_source(payload)
    status = heartbeat_status(payload)
    age = heartbeat_age_seconds(payload)
    elapsed_since_start = time.time() - started_at

    if source is None:
        if elapsed_since_start < SOURCE_READY_GRACE_SEC:
            return False, f"guard heartbeat source not ready yet: {source!r}", 0

        updated_strikes = source_mismatch_strikes + 1
        if updated_strikes >= SOURCE_MISMATCH_STRIKE_LIMIT:
            return True, f"guard heartbeat source mismatch: {source!r}", updated_strikes
        return (
            False,
            (
                f"guard heartbeat source mismatch: {source!r} "
                f"(strike={updated_strikes}/{SOURCE_MISMATCH_STRIKE_LIMIT})"
            ),
            updated_strikes,
        )

    if source != "stop_gate_watcher":
        updated_strikes = source_mismatch_strikes + 1
        if updated_strikes >= SOURCE_MISMATCH_STRIKE_LIMIT:
            return True, f"guard heartbeat source mismatch: {source!r}", updated_strikes
        return (
            False,
            (
                f"guard heartbeat source mismatch: {source!r} "
                f"(strike={updated_strikes}/{SOURCE_MISMATCH_STRIKE_LIMIT})"
            ),
            updated_strikes,
        )

    source_mismatch_strikes = 0

    if status != "alive":
        return True, f"guard heartbeat status is not alive: {status!r}", 0

    if age is None:
        return True, "guard heartbeat age is invalid", 0

    if age > HEARTBEAT_TIMEOUT_SEC:
        return (
            True,
            (
                "guard heartbeat timeout exceeded "
                f"(age={age:.2f}s, timeout={HEARTBEAT_TIMEOUT_SEC:.0f}s)"
            ),
            0,
        )

    if not tmux_session_exists(GUARD_SESSION_NAME):
        return True, "guard tmux session missing", 0

    if not process_exists("CORE_ROOT.stop_gate_watcher"):
        return True, "stop_gate_watcher process missing", 0

    return False, f"guard heartbeat OK (age={age:.2f}s)", 0


def activate_core_kill_chain(reason: str) -> None:
    """Trigger STOP-GATE and terminate the watcher tmux session."""
    log(f"CORE KILL CHAIN ACTIVATED: {reason}")

    subprocess.run(
        ["python3", str(STOP_GATE_SCRIPT), reason],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    subprocess.run(
        ["tmux", "kill-session", "-t", GUARD_SESSION_NAME],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    subprocess.run(
        ["pkill", "-f", "CORE_ROOT.stop_gate_watcher"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    write_self_heartbeat(status="stopped")
    log("CORE KILL CHAIN COMPLETED")


def main() -> None:
    """Run the core guard loop."""
    ensure_runtime_layout()
    log("Core Guard started")

    started_at = time.time()
    source_mismatch_strikes = 0

    try:
        while True:
            write_self_heartbeat(status="alive")

            is_critical, message, source_mismatch_strikes = evaluate_guard(
                started_at=started_at,
                source_mismatch_strikes=source_mismatch_strikes,
            )
            if is_critical:
                activate_core_kill_chain(message)
                break

            log(message)
            time.sleep(POLL_INTERVAL_SEC)

    except KeyboardInterrupt:
        write_self_heartbeat(status="stopped")
        log("Core Guard stopped by user")
    except Exception as exc:  # noqa: BLE001
        activate_core_kill_chain(f"core guard exception: {exc}")


if __name__ == "__main__":
    main()
