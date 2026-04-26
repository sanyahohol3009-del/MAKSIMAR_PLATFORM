from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_dashboard_view import (
    build_foundation_incident_dashboard_view,
)

IncidentsPanelState = Literal[
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
]

ALL_INCIDENTS_PANEL_STATES: tuple[IncidentsPanelState, ...] = (
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
class IncidentsPanelContentEntry:
    """Canonical content entry for the incidents panel."""

    panel_id: str
    panel_state: IncidentsPanelState
    total_incident_entries: int
    active_incident_entries: int
    history_visible_entries: int
    kill_chain_triggered_entries: int
    archived_entries: int
    recovered_entries: int
    critical_entries: int
    warning_entries: int
    info_entries: int
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.panel_state not in ALL_INCIDENTS_PANEL_STATES:
            raise ValueError(
                "panel_state must be one of "
                f"{ALL_INCIDENTS_PANEL_STATES}, got {self.panel_state!r}."
            )

        integer_fields = {
            "total_incident_entries": self.total_incident_entries,
            "active_incident_entries": self.active_incident_entries,
            "history_visible_entries": self.history_visible_entries,
            "kill_chain_triggered_entries": self.kill_chain_triggered_entries,
            "archived_entries": self.archived_entries,
            "recovered_entries": self.recovered_entries,
            "critical_entries": self.critical_entries,
            "warning_entries": self.warning_entries,
            "info_entries": self.info_entries,
        }
        for field_name, field_value in integer_fields.items():
            if field_value < 0:
                raise ValueError(f"{field_name} must be >= 0.")

        if not self.visible_in_main_dashboard:
            raise ValueError(
                "visible_in_main_dashboard must remain true for canonical incidents content."
            )

        if not self.visible_in_oob_dashboard:
            raise ValueError(
                "visible_in_oob_dashboard must remain true for canonical incidents content."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical incidents content."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical incidents content."
            )


@dataclass(frozen=True, slots=True)
class IncidentsPanelContentContract:
    """Canonical content contract for the incidents panel."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    operator_visible_entries: int
    entries: tuple[IncidentsPanelContentEntry, ...]

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


def _derive_incidents_panel_state(
    total_entries: int,
    active_incident_entries: int,
    kill_chain_triggered_entries: int,
    warning_entries: int,
    history_visible_entries: int,
) -> IncidentsPanelState:
    if total_entries == 0:
        return "empty"
    if kill_chain_triggered_entries > 0 or active_incident_entries > 0:
        return "incident"
    if warning_entries > 0:
        return "degraded"
    if history_visible_entries == 0:
        return "loading"
    return "normal"


def build_incidents_panel_content_contract() -> IncidentsPanelContentContract:
    """Build canonical content contract for the incidents panel."""
    incident_dashboard_view = build_foundation_incident_dashboard_view()

    entry = IncidentsPanelContentEntry(
        panel_id="incidents",
        panel_state=_derive_incidents_panel_state(
            total_entries=incident_dashboard_view.total_entries,
            active_incident_entries=incident_dashboard_view.current_incident_entries,
            kill_chain_triggered_entries=incident_dashboard_view.kill_chain_triggered_entries,
            warning_entries=incident_dashboard_view.warning_entries,
            history_visible_entries=incident_dashboard_view.history_visible_entries,
        ),
        total_incident_entries=incident_dashboard_view.total_entries,
        active_incident_entries=incident_dashboard_view.current_incident_entries,
        history_visible_entries=incident_dashboard_view.history_visible_entries,
        kill_chain_triggered_entries=incident_dashboard_view.kill_chain_triggered_entries,
        archived_entries=incident_dashboard_view.archived_entries,
        recovered_entries=incident_dashboard_view.recovered_entries,
        critical_entries=incident_dashboard_view.critical_entries,
        warning_entries=incident_dashboard_view.warning_entries,
        info_entries=incident_dashboard_view.info_entries,
        visible_in_main_dashboard=True,
        visible_in_oob_dashboard=True,
        read_only=True,
        operator_visible=True,
        description=(
            "Canonical incidents panel content contract built from "
            "foundation incident dashboard view."
        ),
    )

    entries = (entry,)

    return IncidentsPanelContentContract(
        contract_id="incidents_panel_content_contract_001",
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
