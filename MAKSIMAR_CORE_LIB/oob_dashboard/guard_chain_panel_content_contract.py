from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_guard_chain_truth_view import (
    build_foundation_guard_chain_truth_view,
)


GuardChainStatus = Literal[
    "consistent",
    "degraded",
]


@dataclass(frozen=True, slots=True)
class GuardChainPanelContentEntry:
    """Canonical content entry for the guard-chain panel."""

    panel_id: str
    total_chain_entries: int
    consistent_chain_entries: int
    degraded_chain_entries: int
    runtime_entry_present: bool
    guard_entry_present: bool
    core_guard_entry_present: bool
    kernel_guard_entry_present: bool
    guard_chain_status: GuardChainStatus
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class GuardChainPanelContentContract:
    """Canonical content contract for the guard-chain panel."""

    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: tuple[GuardChainPanelContentEntry, ...]


def build_guard_chain_panel_content_contract() -> GuardChainPanelContentContract:
    """Build canonical content contract for the guard-chain panel."""
    guard_chain_truth_view = build_foundation_guard_chain_truth_view()

    truth_scopes = {entry.truth_scope for entry in guard_chain_truth_view.entries}

    entries = (
        GuardChainPanelContentEntry(
            panel_id="panel_guard_chain_001",
            total_chain_entries=len(guard_chain_truth_view.entries),
            consistent_chain_entries=sum(
                1
                for entry in guard_chain_truth_view.entries
                if entry.consistency_status == "CONSISTENT"
            ),
            degraded_chain_entries=sum(
                1
                for entry in guard_chain_truth_view.entries
                if entry.derived_status in {"DEGRADED", "BROKEN", "DEAD"}
            ),
            runtime_entry_present="runtime" in truth_scopes,
            guard_entry_present="guard" in truth_scopes,
            core_guard_entry_present="core_guard" in truth_scopes,
            kernel_guard_entry_present="kernel_guard" in truth_scopes,
            guard_chain_status=(
                "consistent"
                if all(
                    entry.consistency_status == "CONSISTENT"
                    for entry in guard_chain_truth_view.entries
                )
                else "degraded"
            ),
            visible_in_main_dashboard=True,
            visible_in_oob_dashboard=True,
            read_only=True,
            description=(
                "Canonical guard-chain panel content contract built from "
                "foundation guard-chain truth view."
            ),
        ),
    )

    return GuardChainPanelContentContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for entry in entries if entry.visible_in_oob_dashboard
        ),
        entries=entries,
    )
