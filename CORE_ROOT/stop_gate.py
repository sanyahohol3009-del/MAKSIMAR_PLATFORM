#!/usr/bin/env python3
"""STOP-GATE trigger for MAKSIMAR foundation services."""

from __future__ import annotations

import sys
import time

from CORE_ROOT.runtime_paths import (
    DEGRADED_MODE_FILE,
    LAST_DEGRADED_REASON_FILE,
    STOP_GATE_TRIGGER_FILE,
    SYSTEM_LOG_FILE,
    ensure_runtime_layout,
)


def log(message: str) -> None:
    """Write a STOP-GATE message to stdout and the shared system log."""
    ensure_runtime_layout()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[STOP-GATE] {timestamp} {message}"
    print(line, flush=True)
    with SYSTEM_LOG_FILE.open("a", encoding="utf-8") as file_obj:
        file_obj.write(line + "\n")


def main() -> None:
    """Record a STOP-GATE activation."""
    ensure_runtime_layout()

    reason = " ".join(sys.argv[1:]).strip() or "stop-gate triggered"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    STOP_GATE_TRIGGER_FILE.write_text(
        f"{timestamp} | {reason}\n",
        encoding="utf-8",
    )
    DEGRADED_MODE_FILE.write_text("1\n", encoding="utf-8")
    LAST_DEGRADED_REASON_FILE.write_text(reason + "\n", encoding="utf-8")

    log(f"ACTIVATED: {reason}")


if __name__ == "__main__":
    main()
