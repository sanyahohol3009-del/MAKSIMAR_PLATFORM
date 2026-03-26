from __future__ import annotations

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
class FoundationLiveStatusDerivedViewEntry:
    """Canonical derived live-status entry for foundation dashboard systems."""

    derived_entry_id: str
    panel_id: str
    truth_scope: FoundationTruthScope
    display_title: str
    status_command: str
    expected_alive_label: str
    expected_dead_label: str
    derived_state: FoundationDerivedState
    signal_path_visible: bool
    execution_stage_visible: bool
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationLiveStatusDerivedViewContract:
    """Canonical derived live-status view contract for foundation dashboard systems."""

    total_entries: int
    alive_entries: int
    dead_entries: int
    degraded_entries: int
    broken_entries: int
    warming_up_entries: int
    signal_visible_entries: int
    execution_stage_visible_entries: int
    entries: tuple[FoundationLiveStatusDerivedViewEntry, ...]


def build_foundation_live_status_derived_view_contract() -> (
    FoundationLiveStatusDerivedViewContract
):
    """Build canonical derived live-status view contract for foundation surfaces."""
    entries = (
        FoundationLiveStatusDerivedViewEntry(
            derived_entry_id="foundationderived_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            truth_scope="runtime",
            display_title="Runtime Core",
            status_command="./tools/ctl status",
            expected_alive_label="ALIVE",
            expected_dead_label="NOT_ALIVE",
            derived_state="ALIVE",
            signal_path_visible=True,
            execution_stage_visible=True,
            read_only=True,
            description=(
                "Canonical derived live-status entry for runtime foundation surface."
            ),
        ),
        FoundationLiveStatusDerivedViewEntry(
            derived_entry_id="foundationderived_guard_001",
            panel_id="panel_foundation_guard_status_001",
            truth_scope="guard",
            display_title="Stop-Gate Watcher",
            status_command="./tools/guard_ctl status",
            expected_alive_label="ALIVE",
            expected_dead_label="NOT_ALIVE",
            derived_state="ALIVE",
            signal_path_visible=True,
            execution_stage_visible=True,
            read_only=True,
            description=(
                "Canonical derived live-status entry for stop-gate watcher surface."
            ),
        ),
        FoundationLiveStatusDerivedViewEntry(
            derived_entry_id="foundationderived_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            truth_scope="core_guard",
            display_title="Core Guard",
            status_command="./tools/core_guard_ctl status",
            expected_alive_label="ALIVE",
            expected_dead_label="NOT_ALIVE",
            derived_state="ALIVE",
            signal_path_visible=True,
            execution_stage_visible=True,
            read_only=True,
            description=(
                "Canonical derived live-status entry for core guard surface."
            ),
        ),
        FoundationLiveStatusDerivedViewEntry(
            derived_entry_id="foundationderived_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            truth_scope="kernel_guard",
            display_title="Kernel Watchdog",
            status_command="./tools/kernel_guard_ctl status",
            expected_alive_label="ALIVE",
            expected_dead_label="NOT_ALIVE",
            derived_state="ALIVE",
            signal_path_visible=True,
            execution_stage_visible=True,
            read_only=True,
            description=(
                "Canonical derived live-status entry for kernel watchdog surface."
            ),
        ),
    )

    return FoundationLiveStatusDerivedViewContract(
        total_entries=len(entries),
        alive_entries=sum(1 for entry in entries if entry.derived_state == "ALIVE"),
        dead_entries=sum(1 for entry in entries if entry.derived_state == "DEAD"),
        degraded_entries=sum(
            1 for entry in entries if entry.derived_state == "DEGRADED"
        ),
        broken_entries=sum(1 for entry in entries if entry.derived_state == "BROKEN"),
        warming_up_entries=sum(
            1 for entry in entries if entry.derived_state == "WARMING_UP"
        ),
        signal_visible_entries=sum(
            1 for entry in entries if entry.signal_path_visible
        ),
        execution_stage_visible_entries=sum(
            1 for entry in entries if entry.execution_stage_visible
        ),
        entries=entries,
    )
