from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_degraded_state_contract import (
    build_foundation_degraded_state_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter import (
    build_foundation_live_status_snapshot,
)


@dataclass(frozen=True)
class FoundationLiveHistoricalStateSplitEntry:
    """Read-only view entry that separates live and historical foundation state."""

    split_entry_id: str
    panel_id: str
    truth_scope: str
    display_title: str
    current_live_state: str
    currently_degraded: bool
    historical_only: bool
    historical_state_visible: bool
    show_as_current_live_state: bool
    degraded_reason: str | None
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationLiveHistoricalStateSplitView:
    """Read-only view for separating live and historical foundation state."""

    view_id: str
    total_entries: int
    live_entries: int
    historical_only_entries: int
    current_degraded_entries: int
    current_live_visible_entries: int
    entries: tuple[FoundationLiveHistoricalStateSplitEntry, ...]


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


def build_foundation_live_historical_state_split_view() -> (
    FoundationLiveHistoricalStateSplitView
):
    """Build read-only view that separates live and historical foundation state."""
    live_snapshot = build_foundation_live_status_snapshot()
    degraded_contract = build_foundation_degraded_state_contract()

    degraded_by_scope = {entry.truth_scope: entry for entry in degraded_contract.entries}

    entries = []
    for live_record in live_snapshot.records:
        degraded_entry = degraded_by_scope[live_record.truth_scope]

        historical_state_visible = degraded_entry.historical_only
        show_as_current_live_state = not degraded_entry.historical_only

        entries.append(
            FoundationLiveHistoricalStateSplitEntry(
                split_entry_id=f"foundationstatesplit_{live_record.truth_scope}_001",
                panel_id=_SCOPE_TO_PANEL[live_record.truth_scope],
                truth_scope=live_record.truth_scope,
                display_title=_SCOPE_TO_TITLE[live_record.truth_scope],
                current_live_state=live_record.derived_state,
                currently_degraded=degraded_entry.is_currently_degraded,
                historical_only=degraded_entry.historical_only,
                historical_state_visible=historical_state_visible,
                show_as_current_live_state=show_as_current_live_state,
                degraded_reason=degraded_entry.degraded_reason,
                read_only=True,
                description=(
                    "Read-only live/historical split view entry derived from live "
                    f"status and degraded-state contract for scope={live_record.truth_scope}."
                ),
            )
        )

    entry_tuple = tuple(entries)

    return FoundationLiveHistoricalStateSplitView(
        view_id="foundation_live_historical_state_split_view_001",
        total_entries=len(entry_tuple),
        live_entries=sum(1 for entry in entry_tuple if not entry.historical_only),
        historical_only_entries=sum(1 for entry in entry_tuple if entry.historical_only),
        current_degraded_entries=sum(
            1 for entry in entry_tuple if entry.currently_degraded
        ),
        current_live_visible_entries=sum(
            1 for entry in entry_tuple if entry.show_as_current_live_state
        ),
        entries=entry_tuple,
    )
