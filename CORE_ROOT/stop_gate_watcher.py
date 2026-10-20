#!/usr/bin/env python3
"""MAKSIMAR STOP-GATE watcher."""

from __future__ import annotations

import signal
import subprocess
import time

from CORE_ROOT.heartbeat_io import (
    atomic_write_json,
    write_guard_heartbeat,
    build_heartbeat,
    heartbeat_age_seconds,
    heartbeat_source,
    heartbeat_status,
    safe_read_json,
)
from CORE_ROOT.runtime_paths import (
    GUARD_HEARTBEAT_FILE,
    GUARD_LOG_FILE,
    PROCESS_SUPERVISOR_SCRIPT,
    RUNTIME_HEARTBEAT_FILE,
    RUNTIME_SESSION_NAME,
    ROOT,
    resolve_canonical_python,
    SYSTEM_LOG_FILE,
    ensure_runtime_layout,
)

HEARTBEAT_TIMEOUT_SEC = 12.0
POLL_INTERVAL_SEC = 2.0
SOURCE_READY_GRACE_SEC = 8.0
SOURCE_MISMATCH_STRIKE_LIMIT = 3


def log(message: str) -> None:
    """Write a watcher log line to stdout and log files."""
    ensure_runtime_layout()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[STOP-GATE-WATCHER] {timestamp} {message}"
    print(line, flush=True)

    for log_file in (GUARD_LOG_FILE, SYSTEM_LOG_FILE):
        with log_file.open("a", encoding="utf-8") as file_obj:
            file_obj.write(line + "\n")


def run_quiet(command: list[str]) -> None:
    """Run subprocess quietly and ignore failures."""
    subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


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


def write_self_heartbeat(status: str = "alive", *, expected_run=None) -> None:
    """Write watcher heartbeat atomically."""
    ensure_runtime_layout()
    write_guard_heartbeat(GUARD_HEARTBEAT_FILE, "stop_gate_watcher", status, expected_run=expected_run)


def evaluate_runtime(
    started_at: float,
    source_mismatch_strikes: int,
) -> tuple[bool, str, int]:
    """Evaluate runtime state.

    Returns:
        (is_critical, message, updated_source_mismatch_strikes)
    """
    payload = safe_read_json(RUNTIME_HEARTBEAT_FILE)
    if payload is None:
        return (
            False,
            f"runtime heartbeat not ready yet: {RUNTIME_HEARTBEAT_FILE}",
            0,
        )

    source = heartbeat_source(payload)
    status = heartbeat_status(payload)
    age = heartbeat_age_seconds(payload)
    elapsed_since_start = time.time() - started_at

    if source is None:
        if elapsed_since_start < SOURCE_READY_GRACE_SEC:
            return False, f"runtime heartbeat source not ready yet: {source!r}", 0

        updated_strikes = source_mismatch_strikes + 1
        if updated_strikes >= SOURCE_MISMATCH_STRIKE_LIMIT:
            return (
                True,
                f"runtime heartbeat source mismatch: {source!r}",
                updated_strikes,
            )
        return (
            False,
            (
                f"runtime heartbeat source mismatch: {source!r} "
                f"(strike={updated_strikes}/{SOURCE_MISMATCH_STRIKE_LIMIT})"
            ),
            updated_strikes,
        )

    if source != "process_supervisor":
        updated_strikes = source_mismatch_strikes + 1
        if updated_strikes >= SOURCE_MISMATCH_STRIKE_LIMIT:
            return (
                True,
                f"runtime heartbeat source mismatch: {source!r}",
                updated_strikes,
            )
        return (
            False,
            (
                f"runtime heartbeat source mismatch: {source!r} "
                f"(strike={updated_strikes}/{SOURCE_MISMATCH_STRIKE_LIMIT})"
            ),
            updated_strikes,
        )

    source_mismatch_strikes = 0

    recovery_deadline = payload.get("recovery_deadline_ts")
    recovery_state = status in {"broken", "booting"} or (status == "alive" and not process_exists("uvicorn"))
    if recovery_state and isinstance(recovery_deadline, (int, float)):
        recovery_remaining = recovery_deadline - time.time()
        if (0 < recovery_remaining <= HEARTBEAT_TIMEOUT_SEC and age is not None
                and age <= HEARTBEAT_TIMEOUT_SEC
                and tmux_session_exists(RUNTIME_SESSION_NAME)
                and process_exists("SUPERVISOR.process_supervisor")):
            return False, f"runtime supervisor bounded recovery ({recovery_remaining:.2f}s remaining)", 0

    if status != "alive":
        return True, f"runtime heartbeat status is not alive: {status!r}", 0

    if age is None:
        return True, "runtime heartbeat age is invalid", 0

    if age > HEARTBEAT_TIMEOUT_SEC:
        return (
            True,
            (
                "runtime heartbeat timeout exceeded "
                f"(age={age:.2f}s, timeout={HEARTBEAT_TIMEOUT_SEC:.0f}s)"
            ),
            0,
        )

    if not tmux_session_exists(RUNTIME_SESSION_NAME):
        return True, "runtime tmux session missing", 0

    if not process_exists("uvicorn"):
        return True, "uvicorn process missing", 0

    return False, f"runtime heartbeat OK (age={age:.2f}s)", 0


def activate_guard_kill_chain(reason: str, *, expected_run=None) -> None:
    """Trigger STOP-GATE and terminate runtime session and process."""
    log(f"GUARD KILL CHAIN ACTIVATED: {reason}")

    run_quiet([str(resolve_canonical_python()), "-m", "CORE_ROOT.stop_gate", reason])
    run_quiet(["tmux", "kill-session", "-t", RUNTIME_SESSION_NAME])
    run_quiet(["pkill", "-f", str(PROCESS_SUPERVISOR_SCRIPT)])
    run_quiet(["pkill", "-f", r"uvicorn .*CONTROL_PLANE\.api_server:app"])

    write_self_heartbeat(status="stopped", expected_run=expected_run)
    log("GUARD KILL CHAIN COMPLETED")


def main() -> None:
    """Run the STOP-GATE watcher loop."""
    ensure_runtime_layout()
    log("Stop-Gate watcher started")

    from CORE_ROOT import run_context
    meta = run_context.read_run_metadata()
    run_identity = run_context._identity(meta) if meta else ()
    stopping = False

    def handle_stop(signum, frame):
        nonlocal stopping
        if not stopping:
            stopping = True
            raise KeyboardInterrupt

    previous_handlers = {sig: signal.getsignal(sig) for sig in
                         (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
    for sig in previous_handlers:
        signal.signal(sig, handle_stop)

    started_at = time.time()
    source_mismatch_strikes = 0
    last_poll_at = time.time()

    try:
        while True:
            write_self_heartbeat(status="alive", expected_run=run_identity)
            poll_gap = time.time() - last_poll_at
            if poll_gap > HEARTBEAT_TIMEOUT_SEC:
                log(f"Observer scheduling gap ({poll_gap:.2f}s); refresh self and recheck after two bounded polls")
                resynchronization_started_at = time.time()
                write_self_heartbeat(status="alive", expected_run=run_identity)
                time.sleep(2 * POLL_INTERVAL_SEC)
                if time.time() - resynchronization_started_at > HEARTBEAT_TIMEOUT_SEC:
                    log("Resynchronization itself was delayed; republish before evaluating peers")
                    continue
            last_poll_at = time.time()

            is_critical, message, source_mismatch_strikes = evaluate_runtime(
                started_at=started_at,
                source_mismatch_strikes=source_mismatch_strikes,
            )
            if is_critical:
                activate_guard_kill_chain(message, expected_run=run_identity)
                break

            log(message)
            time.sleep(POLL_INTERVAL_SEC)

    except KeyboardInterrupt:
        write_self_heartbeat(status="stopped", expected_run=run_identity)
        log("Stop-Gate watcher stopped by user")
    except Exception as exc:  # noqa: BLE001
        activate_guard_kill_chain(f"guard watcher exception: {exc}", expected_run=run_identity)

    finally:
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)


if __name__ == "__main__":
    main()
