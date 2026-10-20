#!/usr/bin/env python3
"""MAKSIMAR kernel watchdog."""

from __future__ import annotations

import signal
import subprocess
import time

from CORE_ROOT.heartbeat_io import (
    atomic_write_json,
    write_guard_heartbeat,
    build_heartbeat,
    heartbeat_age_seconds,
    heartbeat_process_alive,
    heartbeat_source,
    heartbeat_status,
    safe_read_json,
)
from CORE_ROOT.runtime_paths import (
    CORE_GUARD_HEARTBEAT_FILE,
    CORE_GUARD_SESSION_NAME,
    KERNEL_GUARD_LOG_FILE,
    KERNEL_HEARTBEAT_FILE,
    ROOT,
    resolve_canonical_python,
    SYSTEM_LOG_FILE,
    ensure_runtime_layout,
)

HEARTBEAT_TIMEOUT_SEC = 12.0
POLL_INTERVAL_SEC = 2.0
SOURCE_READY_GRACE_SEC = 8.0
SOURCE_MISMATCH_STRIKE_LIMIT = 3
PEER_RESYNCHRONIZATION_LIMIT_SEC = 30.0


def log(message: str) -> None:
    """Write a kernel watchdog log line."""
    ensure_runtime_layout()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[KERNEL-WATCHDOG] {timestamp} {message}"
    print(line, flush=True)

    for log_file in (KERNEL_GUARD_LOG_FILE, SYSTEM_LOG_FILE):
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


def write_kernel_heartbeat(status: str = "alive", *, expected_run=None) -> None:
    """Write the kernel heartbeat atomically."""
    ensure_runtime_layout()
    write_guard_heartbeat(KERNEL_HEARTBEAT_FILE, "kernel_watchdog", status, expected_run=expected_run)


def evaluate_core_guard(
    started_at: float,
    source_mismatch_strikes: int,
    peer_stale_state: dict[str, float] | None = None,
) -> tuple[bool, str, int]:
    """Evaluate the core guard heartbeat."""
    payload = safe_read_json(CORE_GUARD_HEARTBEAT_FILE)
    if payload is None:
        return (
            False,
            f"core guard heartbeat not ready yet: {CORE_GUARD_HEARTBEAT_FILE}",
            0,
        )

    source = heartbeat_source(payload)
    status = heartbeat_status(payload)
    age = heartbeat_age_seconds(payload)
    elapsed_since_start = time.time() - started_at

    if source is None:
        if elapsed_since_start < SOURCE_READY_GRACE_SEC:
            return False, f"core guard heartbeat source not ready yet: {source!r}", 0

        updated_strikes = source_mismatch_strikes + 1
        if updated_strikes >= SOURCE_MISMATCH_STRIKE_LIMIT:
            return (
                True,
                f"core guard heartbeat source mismatch: {source!r}",
                updated_strikes,
            )
        return (
            False,
            (
                f"core guard heartbeat source mismatch: {source!r} "
                f"(strike={updated_strikes}/{SOURCE_MISMATCH_STRIKE_LIMIT})"
            ),
            updated_strikes,
        )

    if source != "core_guard":
        updated_strikes = source_mismatch_strikes + 1
        if updated_strikes >= SOURCE_MISMATCH_STRIKE_LIMIT:
            return (
                True,
                f"core guard heartbeat source mismatch: {source!r}",
                updated_strikes,
            )
        return (
            False,
            (
                f"core guard heartbeat source mismatch: {source!r} "
                f"(strike={updated_strikes}/{SOURCE_MISMATCH_STRIKE_LIMIT})"
            ),
            updated_strikes,
        )

    source_mismatch_strikes = 0

    if status != "alive":
        return True, f"core guard heartbeat status is not alive: {status!r}", 0

    if age is None:
        return True, "core guard heartbeat age is invalid", 0

    if peer_stale_state is not None and age <= HEARTBEAT_TIMEOUT_SEC:
        peer_stale_state.clear()

    if age > HEARTBEAT_TIMEOUT_SEC:
        # A peer can be scheduled later than this observer under resource
        # pressure. Only the exact live peer gets a bounded lease; identity
        # mismatch/death and explicit stopped status never receive one.
        if (peer_stale_state is not None and tmux_session_exists(CORE_GUARD_SESSION_NAME)
                and process_exists("CORE_ROOT.core_guard")
                and heartbeat_process_alive(payload, "CORE_ROOT.core_guard")):
            now = time.monotonic()
            first_observed = peer_stale_state.setdefault("first_stale_observed", now)
            if now - first_observed < PEER_RESYNCHRONIZATION_LIMIT_SEC:
                return False, f"live peer heartbeat delayed; bounded resynchronization ({age:.2f}s)", 0
        return (
            True,
            (
                "core guard heartbeat timeout exceeded "
                f"(age={age:.2f}s, timeout={HEARTBEAT_TIMEOUT_SEC:.0f}s)"
            ),
            0,
        )

    if not tmux_session_exists(CORE_GUARD_SESSION_NAME):
        return True, "core guard tmux session missing", 0

    if not process_exists("CORE_ROOT.core_guard"):
        return True, "core_guard process missing", 0

    return False, f"core guard heartbeat OK (age={age:.2f}s)", 0


def activate_kernel_kill_chain(reason: str, *, expected_run=None) -> None:
    """Trigger STOP-GATE and terminate dependent guard sessions/processes."""
    log(f"KERNEL KILL CHAIN ACTIVATED: {reason}")

    run_quiet([str(resolve_canonical_python()), "-m", "CORE_ROOT.stop_gate", reason])
    run_quiet(["tmux", "kill-session", "-t", CORE_GUARD_SESSION_NAME])
    run_quiet(["pkill", "-f", "CORE_ROOT.core_guard"])
    run_quiet(["pkill", "-f", "CORE_ROOT.stop_gate_watcher"])
    run_quiet(["pkill", "-f", r"uvicorn .*CONTROL_PLANE\.api_server:app"])

    write_kernel_heartbeat(status="stopped", expected_run=expected_run)
    log("KERNEL KILL CHAIN COMPLETED")


def main() -> None:
    """Run the kernel watchdog loop."""
    ensure_runtime_layout()
    log("Kernel Watchdog started")

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
    peer_stale_state: dict[str, float] = {}
    last_poll_at = time.time()

    try:
        while True:
            write_kernel_heartbeat(status="alive", expected_run=run_identity)
            poll_gap = time.time() - last_poll_at
            if poll_gap > HEARTBEAT_TIMEOUT_SEC:
                log(f"Observer scheduling gap ({poll_gap:.2f}s); refresh self and recheck after two bounded polls")
                resynchronization_started_at = time.time()
                write_kernel_heartbeat(status="alive", expected_run=run_identity)
                time.sleep(2 * POLL_INTERVAL_SEC)
                if time.time() - resynchronization_started_at > HEARTBEAT_TIMEOUT_SEC:
                    log("Resynchronization itself was delayed; republish before evaluating peers")
                    continue
            last_poll_at = time.time()

            is_critical, message, source_mismatch_strikes = evaluate_core_guard(
                started_at=started_at,
                source_mismatch_strikes=source_mismatch_strikes,
                peer_stale_state=peer_stale_state,
            )
            if is_critical:
                activate_kernel_kill_chain(message, expected_run=run_identity)
                break

            log(message)
            time.sleep(POLL_INTERVAL_SEC)

    except KeyboardInterrupt:
        write_kernel_heartbeat(status="stopped", expected_run=run_identity)
        log("Kernel Watchdog stopped by user")
    except Exception as exc:  # noqa: BLE001
        activate_kernel_kill_chain(f"kernel watchdog exception: {exc}", expected_run=run_identity)

    finally:
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)


if __name__ == "__main__":
    main()
