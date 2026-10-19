#!/usr/bin/env python3
"""Existing recovery CLI forwarding decisions to the canonical STOP-GATE owner."""

import time

from CORE_ROOT.runtime_paths import SYSTEM_LOG_FILE, ensure_runtime_layout


def log(message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[RECOVERY] {timestamp} {message}"
    print(line, flush=True)
    ensure_runtime_layout()
    with SYSTEM_LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def main() -> None:
    # Preserve the existing CLI/binding surface. Marker ownership, process
    # identity, all heartbeat checks and current-run refusal stay canonical.
    from CORE_ROOT.stop_gate import recover_previous_run_degradation

    try:
        if recover_previous_run_degradation():
            log("Recovery OK: canonical previous-run recovery accepted")
        else:
            log("Recovery skipped: canonical recovery refused; diagnostics preserved")
    except Exception as exc:
        log(f"Recovery manager failed: {exc}")


if __name__ == "__main__":
    main()
