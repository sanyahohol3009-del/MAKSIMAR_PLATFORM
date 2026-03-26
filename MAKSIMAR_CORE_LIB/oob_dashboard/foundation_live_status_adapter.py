from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Literal


FoundationDerivedState = Literal[
    "ALIVE",
    "DEAD",
    "DEGRADED",
    "BROKEN",
    "WARMING_UP",
]

FoundationTruthScope = Literal[
    "runtime",
    "guard",
    "core_guard",
    "kernel_guard",
]


@dataclass(frozen=True)
class FoundationLiveStatusRecord:
    """Normalized live status record for a single foundation surface."""

    truth_scope: FoundationTruthScope
    display_title: str
    status_command: str
    derived_state: FoundationDerivedState
    raw_output: str
    command_succeeded: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    read_only: bool


@dataclass(frozen=True)
class FoundationLiveStatusSnapshot:
    """Normalized live status snapshot across all foundation surfaces."""

    total_records: int
    alive_records: int
    dead_records: int
    degraded_records: int
    broken_records: int
    warming_up_records: int
    records: tuple[FoundationLiveStatusRecord, ...]


def _normalize_status_output(output: str) -> FoundationDerivedState:
    """Normalize shell status output into canonical derived state."""
    normalized = output.upper()

    if "STATE:" in normalized and "DEGRADED" in normalized:
        return "DEGRADED"

    if "STATE:" in normalized and "ALIVE" in normalized:
        return "ALIVE"

    if "STATE:" in normalized and "DEAD" in normalized:
        return "DEAD"

    if "STATE:" in normalized and "WARMING_UP" in normalized:
        return "WARMING_UP"

    if "TRUTH:" in normalized and "ALIVE" in normalized:
        return "ALIVE"

    if "TRUTH:" in normalized and "NOT_ALIVE" in normalized:
        return "DEAD"

    return "BROKEN"


def _run_status_command(command: str) -> tuple[str, bool]:
    """Run a foundation status command and return output plus success flag."""
    completed = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )

    combined_output = completed.stdout
    if completed.stderr:
        if combined_output:
            combined_output += "\n"
        combined_output += completed.stderr

    return combined_output.strip(), completed.returncode == 0


def _build_record(
    *,
    truth_scope: FoundationTruthScope,
    display_title: str,
    status_command: str,
) -> FoundationLiveStatusRecord:
    """Build a normalized live status record."""
    output, succeeded = _run_status_command(status_command)
    derived_state = _normalize_status_output(output)

    if not succeeded and derived_state == "ALIVE":
        derived_state = "BROKEN"

    return FoundationLiveStatusRecord(
        truth_scope=truth_scope,
        display_title=display_title,
        status_command=status_command,
        derived_state=derived_state,
        raw_output=output,
        command_succeeded=succeeded,
        signal_path_visible=True,
        execution_stage_visible=True,
        read_only=True,
    )


def build_foundation_live_status_snapshot() -> FoundationLiveStatusSnapshot:
    """Build normalized live foundation status snapshot from current shell surfaces."""
    records = (
        _build_record(
            truth_scope="runtime",
            display_title="Runtime Core",
            status_command="./tools/ctl status",
        ),
        _build_record(
            truth_scope="guard",
            display_title="Stop-Gate Watcher",
            status_command="./tools/guard_ctl status",
        ),
        _build_record(
            truth_scope="core_guard",
            display_title="Core Guard",
            status_command="./tools/core_guard_ctl status",
        ),
        _build_record(
            truth_scope="kernel_guard",
            display_title="Kernel Watchdog",
            status_command="./tools/kernel_guard_ctl status",
        ),
    )

    return FoundationLiveStatusSnapshot(
        total_records=len(records),
        alive_records=sum(1 for record in records if record.derived_state == "ALIVE"),
        dead_records=sum(1 for record in records if record.derived_state == "DEAD"),
        degraded_records=sum(
            1 for record in records if record.derived_state == "DEGRADED"
        ),
        broken_records=sum(1 for record in records if record.derived_state == "BROKEN"),
        warming_up_records=sum(
            1 for record in records if record.derived_state == "WARMING_UP"
        ),
        records=records,
    )
