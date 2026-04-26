from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_guard_chain_truth_view import (
    build_foundation_guard_chain_truth_view,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_historical_state_split_view import (
    build_foundation_live_historical_state_split_view,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view import (
    build_foundation_truth_consistency_view,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view import (
    build_foundation_unified_dashboard_view,
)

GuardChainPanelState = Literal[
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
]

ALL_GUARD_CHAIN_PANEL_STATES: tuple[GuardChainPanelState, ...] = (
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GuardChainPanelContentEntry:
    """Canonical content entry for the guard-chain panel."""

    panel_id: str
    panel_state: GuardChainPanelState
    total_chain_entries: int
    consistent_chain_entries: int
    partial_chain_entries: int
    mismatch_chain_entries: int
    unknown_chain_entries: int
    alive_chain_entries: int
    degraded_chain_entries: int
    dead_chain_entries: int
    broken_chain_entries: int
    warming_up_panels: int
    historical_only_panels: int
    runtime_entry_present: bool
    guard_entry_present: bool
    core_guard_entry_present: bool
    kernel_guard_entry_present: bool
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.panel_state not in ALL_GUARD_CHAIN_PANEL_STATES:
            raise ValueError(
                "panel_state must be one of "
                f"{ALL_GUARD_CHAIN_PANEL_STATES}, got {self.panel_state!r}."
            )

        integer_fields = {
            "total_chain_entries": self.total_chain_entries,
            "consistent_chain_entries": self.consistent_chain_entries,
            "partial_chain_entries": self.partial_chain_entries,
            "mismatch_chain_entries": self.mismatch_chain_entries,
            "unknown_chain_entries": self.unknown_chain_entries,
            "alive_chain_entries": self.alive_chain_entries,
            "degraded_chain_entries": self.degraded_chain_entries,
            "dead_chain_entries": self.dead_chain_entries,
            "broken_chain_entries": self.broken_chain_entries,
            "warming_up_panels": self.warming_up_panels,
            "historical_only_panels": self.historical_only_panels,
        }
        for field_name, field_value in integer_fields.items():
            if field_value < 0:
                raise ValueError(f"{field_name} must be >= 0.")

        if not self.visible_in_main_dashboard:
            raise ValueError(
                "visible_in_main_dashboard must remain true for canonical guard-chain content."
            )

        if not self.visible_in_oob_dashboard:
            raise ValueError(
                "visible_in_oob_dashboard must remain true for canonical guard-chain content."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical guard-chain content."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical guard-chain content."
            )

        required_presence = (
            self.runtime_entry_present,
            self.guard_entry_present,
            self.core_guard_entry_present,
            self.kernel_guard_entry_present,
        )
        if self.total_chain_entries > 0 and not all(required_presence):
            raise ValueError(
                "canonical guard-chain content requires runtime/guard/core_guard/kernel_guard presence."
            )


@dataclass(frozen=True, slots=True)
class GuardChainPanelContentContract:
    """Canonical content contract for the guard-chain panel."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    operator_visible_entries: int
    entries: tuple[GuardChainPanelContentEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_entries != sum(1 for entry in self.entries if entry.read_only):
            raise ValueError("read_only_entries must match read_only count.")

        if self.main_dashboard_visible_entries != sum(
            1 for entry in self.entries if entry.visible_in_main_dashboard
        ):
            raise ValueError(
                "main_dashboard_visible_entries must match visible_in_main_dashboard count."
            )

        if self.oob_visible_entries != sum(
            1 for entry in self.entries if entry.visible_in_oob_dashboard
        ):
            raise ValueError(
                "oob_visible_entries must match visible_in_oob_dashboard count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def _derive_guard_chain_panel_state(
    total_entries: int,
    broken_entries: int,
    dead_entries: int,
    degraded_entries: int,
    mismatch_entries: int,
    warming_up_panels: int,
    historical_only_panels: int,
) -> GuardChainPanelState:
    if total_entries == 0:
        return "empty"
    if warming_up_panels > 0:
        return "loading"
    if broken_entries > 0 or dead_entries > 0:
        return "incident"
    if mismatch_entries > 0:
        return "stale"
    if historical_only_panels > 0 or degraded_entries > 0:
        return "degraded"
    return "normal"


def build_guard_chain_panel_content_contract() -> GuardChainPanelContentContract:
    """Build canonical content contract for the guard-chain panel."""
    guard_chain_truth_view = build_foundation_guard_chain_truth_view()
    unified_dashboard_view = build_foundation_unified_dashboard_view()
    live_historical_view = build_foundation_live_historical_state_split_view()
    truth_consistency_view = build_foundation_truth_consistency_view()

    truth_scopes = {entry.truth_scope for entry in guard_chain_truth_view.entries}

    entry = GuardChainPanelContentEntry(
        panel_id="guard_chain",
        panel_state=_derive_guard_chain_panel_state(
            total_entries=guard_chain_truth_view.total_entries,
            broken_entries=guard_chain_truth_view.broken_entries,
            dead_entries=guard_chain_truth_view.dead_entries,
            degraded_entries=guard_chain_truth_view.degraded_entries,
            mismatch_entries=truth_consistency_view.mismatch_entries,
            warming_up_panels=unified_dashboard_view.warming_up_panels,
            historical_only_panels=live_historical_view.historical_only_entries,
        ),
        total_chain_entries=guard_chain_truth_view.total_entries,
        consistent_chain_entries=guard_chain_truth_view.consistent_entries,
        partial_chain_entries=guard_chain_truth_view.partial_entries,
        mismatch_chain_entries=guard_chain_truth_view.mismatch_entries,
        unknown_chain_entries=guard_chain_truth_view.unknown_entries,
        alive_chain_entries=guard_chain_truth_view.alive_entries,
        degraded_chain_entries=guard_chain_truth_view.degraded_entries,
        dead_chain_entries=guard_chain_truth_view.dead_entries,
        broken_chain_entries=guard_chain_truth_view.broken_entries,
        warming_up_panels=unified_dashboard_view.warming_up_panels,
        historical_only_panels=live_historical_view.historical_only_entries,
        runtime_entry_present="runtime" in truth_scopes,
        guard_entry_present="guard" in truth_scopes,
        core_guard_entry_present="core_guard" in truth_scopes,
        kernel_guard_entry_present="kernel_guard" in truth_scopes,
        visible_in_main_dashboard=True,
        visible_in_oob_dashboard=True,
        read_only=True,
        operator_visible=True,
        description=(
            "Canonical guard-chain panel content contract derived from "
            "foundation guard-chain truth view, foundation unified dashboard view, "
            "foundation live/historical split view, and foundation truth consistency view."
        ),
    )

    entries = (entry,)

    return GuardChainPanelContentContract(
        contract_id="guard_chain_panel_content_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for item in entries if item.read_only),
        main_dashboard_visible_entries=sum(
            1 for item in entries if item.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for item in entries if item.visible_in_oob_dashboard
        ),
        operator_visible_entries=sum(
            1 for item in entries if item.operator_visible
        ),
        entries=entries,
    )
