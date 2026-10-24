from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view import (
    build_foundation_truth_consistency_view,
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
    total_panels: int, degraded_panels: int, broken_panels: int,
    warming_up_panels: int, truth_mismatch_panels: int, historical_only_panels: int,
    *, dead_panels: int = 0, unknown_panels: int = 0, partial_panels: int = 0,
    alive_panels: int = 0, consistent_panels: int = 0,
) -> SystemStatusPanelState:
    if broken_panels > 0 or dead_panels > 0:
        return "incident"
    if total_panels == 0:
        return "empty"
    if truth_mismatch_panels > 0:
        return "stale"
    if (total_panels != 4 or unknown_panels > 0 or partial_panels > 0
            or historical_only_panels > 0 or degraded_panels > 0):
        return "degraded"
    if warming_up_panels > 0:
        return "loading"
    return "normal" if alive_panels == total_panels == consistent_panels else "degraded"


def build_system_status_panel_content_contract(observation: dict | None = None) -> SystemStatusPanelContentContract:
    """Build canonical content contract for the system-status panel."""
    truth_consistency_view = build_foundation_truth_consistency_view(observation=observation)
    statuses = [item.derived_status for item in truth_consistency_view.entries]
    historical = (4 if isinstance(observation, dict) and observation.get("historical_only") is True else 0)
    current_visible = sum(value != "UNKNOWN" for value in statuses) if not historical else 0

    entry = SystemStatusPanelContentEntry(
        panel_id="system_status",
        panel_state=_derive_panel_state(
            total_panels=truth_consistency_view.total_entries,
            degraded_panels=statuses.count("DEGRADED"),
            broken_panels=statuses.count("BROKEN"),
            warming_up_panels=statuses.count("WARMING_UP"),
            truth_mismatch_panels=truth_consistency_view.mismatch_entries,
            historical_only_panels=historical,
            dead_panels=statuses.count("DEAD"),
            unknown_panels=sum(item.derived_status == "UNKNOWN" for item in truth_consistency_view.entries),
            partial_panels=truth_consistency_view.partial_entries,
            alive_panels=statuses.count("ALIVE"),
            consistent_panels=truth_consistency_view.consistent_entries,
        ),
        total_foundation_panels=truth_consistency_view.total_entries,
        alive_panels=statuses.count("ALIVE"),
        degraded_panels=statuses.count("DEGRADED"),
        broken_panels=statuses.count("BROKEN"),
        warming_up_panels=statuses.count("WARMING_UP"),
        truth_consistent_panels=truth_consistency_view.consistent_entries,
        truth_partial_panels=truth_consistency_view.partial_entries,
        truth_mismatch_panels=truth_consistency_view.mismatch_entries,
        historical_only_panels=historical,
        current_live_visible_panels=current_visible,
        visible_in_main_dashboard=True,
        visible_in_oob_dashboard=True,
        read_only=True,
        operator_visible=True,
        description=(
            "Canonical system-status panel content contract derived from "
            "one canonical observation and "
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
