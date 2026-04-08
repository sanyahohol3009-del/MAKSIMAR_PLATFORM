from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visible_state_contract import (
    build_operator_dashboard_visible_state_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_visible_presentation_contract import (
    build_operator_visible_presentation_contract,
)


ScreenStateStatus = Literal[
    "screen_state_ready",
]

ScreenStateClass = Literal[
    "main_operator_screen_state",
]

ALL_SCREEN_STATE_STATUSES: tuple[ScreenStateStatus, ...] = (
    "screen_state_ready",
)

ALL_SCREEN_STATE_CLASSES: tuple[ScreenStateClass, ...] = (
    "main_operator_screen_state",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardScreenStateEntry:
    """Canonical operator dashboard screen-state entry."""

    screen_state_id: str
    dashboard_id: str
    workspace_id: str
    screen_state_status: ScreenStateStatus
    screen_state_class: ScreenStateClass
    visible_state_ready: bool
    presentation_entries: int
    shared_surface_entries: int
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard screen-state entry."""
        _require_non_empty(self.screen_state_id, "screen_state_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.screen_state_status not in ALL_SCREEN_STATE_STATUSES:
            raise ValueError(
                "screen_state_status must be one of "
                f"{ALL_SCREEN_STATE_STATUSES}, got {self.screen_state_status!r}."
            )

        if self.screen_state_class not in ALL_SCREEN_STATE_CLASSES:
            raise ValueError(
                "screen_state_class must be one of "
                f"{ALL_SCREEN_STATE_CLASSES}, got {self.screen_state_class!r}."
            )

        if not self.visible_state_ready:
            raise ValueError(
                "visible_state_ready must remain true for canonical dashboard screen-state entries."
            )

        if self.presentation_entries < 1:
            raise ValueError(
                "presentation_entries must be at least 1 for canonical dashboard screen-state entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical dashboard screen-state entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardScreenStateContract:
    """Canonical operator dashboard screen-state contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardScreenStateEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard screen-state contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.screen_state_status == "screen_state_ready"
        ):
            raise ValueError(
                "ready_entries must match screen_state_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_screen_state_contract() -> OperatorDashboardScreenStateContract:
    """Build canonical operator dashboard screen-state contract."""
    visible_state_contract = build_operator_dashboard_visible_state_contract()
    presentation_contract = build_operator_visible_presentation_contract()

    visible_entry = visible_state_contract.entries[0]

    entries = (
        OperatorDashboardScreenStateEntry(
            screen_state_id="operator_dashboard_screen_state_001",
            dashboard_id=visible_entry.dashboard_id,
            workspace_id=visible_entry.workspace_id,
            screen_state_status="screen_state_ready",
            screen_state_class="main_operator_screen_state",
            visible_state_ready=visible_entry.bundle_ready,
            presentation_entries=presentation_contract.total_entries,
            shared_surface_entries=presentation_contract.shared_surface_entries,
            operator_visible=True,
            description=(
                "Canonical operator dashboard screen-state entry assembled from "
                "visible dashboard state and operator-visible presentation entries."
            ),
        ),
    )

    return OperatorDashboardScreenStateContract(
        contract_id="operator_dashboard_screen_state_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_state_status == "screen_state_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
