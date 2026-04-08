from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_presentation_bundle_contract import (
    build_operator_presentation_bundle_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)


VisibleDashboardState = Literal[
    "dashboard_visible_ready",
]

VisibleDashboardClass = Literal[
    "main_operator_visible_dashboard",
]

ALL_VISIBLE_DASHBOARD_STATES: tuple[VisibleDashboardState, ...] = (
    "dashboard_visible_ready",
)

ALL_VISIBLE_DASHBOARD_CLASSES: tuple[VisibleDashboardClass, ...] = (
    "main_operator_visible_dashboard",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisibleStateEntry:
    """Canonical operator dashboard visible-state entry."""

    visible_state_id: str
    dashboard_id: str
    workspace_id: str
    visible_dashboard_state: VisibleDashboardState
    visible_dashboard_class: VisibleDashboardClass
    bundle_ready: bool
    presentation_entries: int
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard visible-state entry."""
        _require_non_empty(self.visible_state_id, "visible_state_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.visible_dashboard_state not in ALL_VISIBLE_DASHBOARD_STATES:
            raise ValueError(
                "visible_dashboard_state must be one of "
                f"{ALL_VISIBLE_DASHBOARD_STATES}, got {self.visible_dashboard_state!r}."
            )

        if self.visible_dashboard_class not in ALL_VISIBLE_DASHBOARD_CLASSES:
            raise ValueError(
                "visible_dashboard_class must be one of "
                f"{ALL_VISIBLE_DASHBOARD_CLASSES}, got {self.visible_dashboard_class!r}."
            )

        if not self.bundle_ready:
            raise ValueError(
                "bundle_ready must remain true for canonical dashboard visible-state entries."
            )

        if self.presentation_entries < 1:
            raise ValueError(
                "presentation_entries must be at least 1 for canonical dashboard visible-state entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical dashboard visible-state entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardVisibleStateContract:
    """Canonical operator dashboard visible-state contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardVisibleStateEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard visible-state contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.visible_dashboard_state == "dashboard_visible_ready"
        ):
            raise ValueError(
                "ready_entries must match dashboard_visible_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_visible_state_contract() -> OperatorDashboardVisibleStateContract:
    """Build canonical operator dashboard visible-state contract."""
    bundle_contract = build_operator_presentation_bundle_contract()
    dashboard_contract = build_main_operator_dashboard_contract()

    bundle_entry = bundle_contract.entries[0]
    dashboard_entry = dashboard_contract.entries[0]

    entries = (
        OperatorDashboardVisibleStateEntry(
            visible_state_id="operator_dashboard_visible_state_001",
            dashboard_id=dashboard_entry.dashboard_id,
            workspace_id=dashboard_entry.workspace_id,
            visible_dashboard_state="dashboard_visible_ready",
            visible_dashboard_class="main_operator_visible_dashboard",
            bundle_ready=bundle_entry.bundle_state == "operator_bundle_ready",
            presentation_entries=bundle_entry.presentation_entries,
            operator_visible=True,
            description=(
                "Canonical operator dashboard visible-state entry assembled from "
                "the operator presentation bundle and main operator dashboard."
            ),
        ),
    )

    return OperatorDashboardVisibleStateContract(
        contract_id="operator_dashboard_visible_state_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.visible_dashboard_state == "dashboard_visible_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
