from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_historical_state_split_view import (
    build_foundation_live_historical_state_split_view,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view import (
    build_foundation_truth_consistency_view,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view import (
    build_foundation_unified_dashboard_view,
)

SystemStatusPanelState = Literal[
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
]

ALL_SYSTEM_STATUS_PANEL_STATES: tuple[SystemStatusPanelState, ...] = (
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class SystemStatusPanelContentEntry:
    """Canonical content entry for the system-status panel."""

    panel_id: str
    panel_state: SystemStatusPanelState
    total_foundation_panels: int
    alive_panels: int
    degraded_panels: int
    broken_panels: int
    warming_up_panels: int
    truth_consistent_panels: int
    truth_partial_panels: int
    truth_mismatch_panels: int
    historical_only_panels: int
    current_live_visible_panels: int
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.panel_state not in ALL_SYSTEM_STATUS_PANEL_STATES:
            raise ValueError(
                "panel_state must be one of "
                f"{ALL_SYSTEM_STATUS_PANEL_STATES}, got {self.panel_state!r}."
            )

        integer_fields = {
            "total_foundation_panels": self.total_foundation_panels,
            "alive_panels": self.alive_panels,
            "degraded_panels": self.degraded_panels,
            "broken_panels": self.broken_panels,
            "warming_up_panels": self.warming_up_panels,
            "truth_consistent_panels": self.truth_consistent_panels,
            "truth_partial_panels": self.truth_partial_panels,
            "truth_mismatch_panels": self.truth_mismatch_panels,
            "historical_only_panels": self.historical_only_panels,
            "current_live_visible_panels": self.current_live_visible_panels,
        }
        for field_name, field_value in integer_fields.items():
            if field_value < 0:
                raise ValueError(f"{field_name} must be >= 0.")

        if not self.visible_in_main_dashboard:
            raise ValueError(
                "visible_in_main_dashboard must remain true for canonical system-status content."
            )

        if not self.visible_in_oob_dashboard:
            raise ValueError(
                "visible_in_oob_dashboard must remain true for canonical system-status content."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical system-status content."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical system-status content."
            )


@dataclass(frozen=True, slots=True)
class SystemStatusPanelContentContract:
    """Canonical content contract for the system-status panel."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    operator_visible_entries: int
    entries: tuple[SystemStatusPanelContentEntry, ...]

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


def _derive_panel_state(
    total_panels: int,
    degraded_panels: int,
    broken_panels: int,
    warming_up_panels: int,
    truth_mismatch_panels: int,
    historical_only_panels: int,
) -> SystemStatusPanelState:
    """Derive canonical system-status panel state."""
    if total_panels == 0:
        return "empty"
    if warming_up_panels > 0:
        return "loading"
    if broken_panels > 0:
        return "incident"
    if truth_mismatch_panels > 0:
        return "stale"
    if historical_only_panels > 0 or degraded_panels > 0:
        return "degraded"
    return "normal"


def build_system_status_panel_content_contract() -> SystemStatusPanelContentContract:
    """Build canonical content contract for the system-status panel."""
    unified_dashboard_view = build_foundation_unified_dashboard_view()
    live_historical_view = build_foundation_live_historical_state_split_view()
    truth_consistency_view = build_foundation_truth_consistency_view()

    entry = SystemStatusPanelContentEntry(
        panel_id="system_status",
        panel_state=_derive_panel_state(
            total_panels=unified_dashboard_view.total_panels,
            degraded_panels=unified_dashboard_view.degraded_panels,
            broken_panels=unified_dashboard_view.broken_panels,
            warming_up_panels=unified_dashboard_view.warming_up_panels,
            truth_mismatch_panels=truth_consistency_view.mismatch_entries,
            historical_only_panels=live_historical_view.historical_only_entries,
        ),
        total_foundation_panels=unified_dashboard_view.total_panels,
        alive_panels=unified_dashboard_view.alive_panels,
        degraded_panels=unified_dashboard_view.degraded_panels,
        broken_panels=unified_dashboard_view.broken_panels,
        warming_up_panels=unified_dashboard_view.warming_up_panels,
        truth_consistent_panels=truth_consistency_view.consistent_entries,
        truth_partial_panels=truth_consistency_view.partial_entries,
        truth_mismatch_panels=truth_consistency_view.mismatch_entries,
        historical_only_panels=live_historical_view.historical_only_entries,
        current_live_visible_panels=live_historical_view.current_live_visible_entries,
        visible_in_main_dashboard=True,
        visible_in_oob_dashboard=True,
        read_only=True,
        operator_visible=True,
        description=(
            "Canonical system-status panel content contract derived from "
            "foundation unified dashboard view, live/historical split view, "
            "and truth consistency view."
        ),
    )

    entries = (entry,)

    return SystemStatusPanelContentContract(
        contract_id="system_status_panel_content_contract_001",
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
