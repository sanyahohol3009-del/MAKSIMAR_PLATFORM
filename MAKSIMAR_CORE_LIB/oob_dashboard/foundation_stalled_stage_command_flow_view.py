from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter import (
    build_foundation_live_status_snapshot,
)


FoundationTruthScope = Literal[
    "runtime",
    "guard",
    "core_guard",
    "kernel_guard",
]

FoundationCommandStage = Literal[
    "runtime_execution",
    "stop_gate_watch",
    "core_guard_enforcement",
    "kernel_watchdog_supervision",
]

FoundationFlowState = Literal[
    "FLOWING",
    "STALLED",
    "BROKEN",
    "IDLE",
]


@dataclass(frozen=True)
class FoundationStalledStageCommandFlowEntry:
    """Canonical stalled-stage / command-flow entry for foundation dashboards."""

    flow_entry_id: str
    panel_id: str
    truth_scope: FoundationTruthScope
    display_title: str
    command_stage: FoundationCommandStage
    derived_state: str
    flow_state: FoundationFlowState
    command_flow_visible: bool
    stalled_stage_visible: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    suspected_source_file: str
    description: str


@dataclass(frozen=True)
class FoundationStalledStageCommandFlowView:
    """Canonical stalled-stage / command-flow view for foundation dashboards."""

    view_id: str
    total_entries: int
    flowing_entries: int
    stalled_entries: int
    broken_entries: int
    idle_entries: int
    command_flow_visible_entries: int
    stalled_stage_visible_entries: int
    entries: tuple[FoundationStalledStageCommandFlowEntry, ...]


_SCOPE_TO_PANEL = {
    "runtime": "panel_foundation_runtime_status_001",
    "guard": "panel_foundation_guard_status_001",
    "core_guard": "panel_foundation_core_guard_status_001",
    "kernel_guard": "panel_foundation_kernel_guard_status_001",
}

_SCOPE_TO_TITLE = {
    "runtime": "Runtime Core",
    "guard": "Stop-Gate Watcher",
    "core_guard": "Core Guard",
    "kernel_guard": "Kernel Watchdog",
}

_SCOPE_TO_STAGE = {
    "runtime": "runtime_execution",
    "guard": "stop_gate_watch",
    "core_guard": "core_guard_enforcement",
    "kernel_guard": "kernel_watchdog_supervision",
}

_SCOPE_TO_SOURCE_FILE = {
    "runtime": "SUPERVISOR/process_supervisor.py",
    "guard": "CORE_ROOT/stop_gate_watcher.py",
    "core_guard": "CORE_ROOT/core_guard.py",
    "kernel_guard": "CORE_ROOT/kernel_watchdog.py",
}


def _flow_state_for_derived_state(derived_state: str) -> FoundationFlowState:
    """Map derived foundation state to command-flow state."""
    if derived_state == "ALIVE":
        return "FLOWING"
    if derived_state == "WARMING_UP":
        return "IDLE"
    if derived_state == "DEGRADED":
        return "STALLED"
    if derived_state in {"DEAD", "BROKEN"}:
        return "BROKEN"
    return "STALLED"


def _stalled_stage_visible_for_flow_state(flow_state: FoundationFlowState) -> bool:
    """Return whether stalled-stage visibility should be enabled."""
    return flow_state in {"STALLED", "BROKEN"}


def build_foundation_stalled_stage_command_flow_view() -> (
    FoundationStalledStageCommandFlowView
):
    """Build canonical stalled-stage / command-flow view from live foundation state."""
    snapshot = build_foundation_live_status_snapshot()

    entries = []
    for record in snapshot.records:
        truth_scope = record.truth_scope
        derived_state = record.derived_state
        flow_state = _flow_state_for_derived_state(derived_state)

        entries.append(
            FoundationStalledStageCommandFlowEntry(
                flow_entry_id=f"foundationflow_{truth_scope}_001",
                panel_id=_SCOPE_TO_PANEL[truth_scope],
                truth_scope=truth_scope,
                display_title=_SCOPE_TO_TITLE[truth_scope],
                command_stage=_SCOPE_TO_STAGE[truth_scope],
                derived_state=derived_state,
                flow_state=flow_state,
                command_flow_visible=True,
                stalled_stage_visible=_stalled_stage_visible_for_flow_state(
                    flow_state
                ),
                signal_path_visible=True,
                execution_stage_visible=True,
                suspected_source_file=_SCOPE_TO_SOURCE_FILE[truth_scope],
                description=(
                    "Canonical stalled-stage / command-flow entry derived from "
                    f"live foundation status for scope={truth_scope}."
                ),
            )
        )

    entry_tuple = tuple(entries)

    return FoundationStalledStageCommandFlowView(
        view_id="foundation_stalled_stage_command_flow_view_001",
        total_entries=len(entry_tuple),
        flowing_entries=sum(1 for entry in entry_tuple if entry.flow_state == "FLOWING"),
        stalled_entries=sum(1 for entry in entry_tuple if entry.flow_state == "STALLED"),
        broken_entries=sum(1 for entry in entry_tuple if entry.flow_state == "BROKEN"),
        idle_entries=sum(1 for entry in entry_tuple if entry.flow_state == "IDLE"),
        command_flow_visible_entries=sum(
            1 for entry in entry_tuple if entry.command_flow_visible
        ),
        stalled_stage_visible_entries=sum(
            1 for entry in entry_tuple if entry.stalled_stage_visible
        ),
        entries=entry_tuple,
    )
