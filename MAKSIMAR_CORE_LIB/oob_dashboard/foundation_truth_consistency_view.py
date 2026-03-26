from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_contract import (
    build_foundation_truth_consistency_contract,
)


@dataclass(frozen=True)
class FoundationTruthConsistencyViewEntry:
    """Read-only dashboard view entry for foundation truth consistency."""

    view_entry_id: str
    panel_id: str
    truth_scope: str
    display_title: str
    derived_status: str
    consistency_status: str
    heartbeat_truth: bool
    process_truth: bool
    session_truth: bool
    api_truth: bool
    log_truth: bool
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationTruthConsistencyView:
    """Read-only dashboard view for foundation truth consistency."""

    view_id: str
    total_entries: int
    consistent_entries: int
    partial_entries: int
    mismatch_entries: int
    unknown_entries: int
    entries: tuple[FoundationTruthConsistencyViewEntry, ...]


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


def build_foundation_truth_consistency_view() -> FoundationTruthConsistencyView:
    """Build read-only dashboard view from foundation truth consistency contract."""
    contract = build_foundation_truth_consistency_contract()

    entries = tuple(
        FoundationTruthConsistencyViewEntry(
            view_entry_id=f"foundationtruthview_{entry.truth_scope}_001",
            panel_id=_SCOPE_TO_PANEL[entry.truth_scope],
            truth_scope=entry.truth_scope,
            display_title=_SCOPE_TO_TITLE[entry.truth_scope],
            derived_status=entry.derived_status,
            consistency_status=entry.consistency_status,
            heartbeat_truth=entry.heartbeat_truth,
            process_truth=entry.process_truth,
            session_truth=entry.session_truth,
            api_truth=entry.api_truth,
            log_truth=entry.log_truth,
            read_only=True,
            description=(
                "Read-only foundation truth consistency view entry derived from "
                f"consistency contract for scope={entry.truth_scope}."
            ),
        )
        for entry in contract.entries
    )

    return FoundationTruthConsistencyView(
        view_id="foundation_truth_consistency_view_001",
        total_entries=len(entries),
        consistent_entries=sum(
            1 for entry in entries if entry.consistency_status == "CONSISTENT"
        ),
        partial_entries=sum(
            1 for entry in entries if entry.consistency_status == "PARTIAL"
        ),
        mismatch_entries=sum(
            1 for entry in entries if entry.consistency_status == "MISMATCH"
        ),
        unknown_entries=sum(
            1 for entry in entries if entry.consistency_status == "UNKNOWN"
        ),
        entries=entries,
    )
