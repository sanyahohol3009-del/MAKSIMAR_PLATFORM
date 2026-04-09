from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_session_restore_contract import (
    build_dashboard_session_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_restore_contract import (
    build_display_assignment_restore_contract,
)


PanelPlacementRestoreState = Literal[
    "panel_placement_restore_ready",
]

PanelPlacementRestoreClass = Literal[
    "dashboard_panel_placement_restore",
]

ALL_PANEL_PLACEMENT_RESTORE_STATES: tuple[PanelPlacementRestoreState, ...] = (
    "panel_placement_restore_ready",
)

ALL_PANEL_PLACEMENT_RESTORE_CLASSES: tuple[PanelPlacementRestoreClass, ...] = (
    "dashboard_panel_placement_restore",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PanelPlacementRestoreEntry:
    """Canonical panel placement restore entry."""

    panel_placement_restore_id: str
    workspace_id: str
    panel_placement_restore_state: PanelPlacementRestoreState
    panel_placement_restore_class: PanelPlacementRestoreClass
    dashboard_session_restore_ready: bool
    display_assignment_restore_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical panel placement restore entry."""
        _require_non_empty(
            self.panel_placement_restore_id, "panel_placement_restore_id"
        )
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.panel_placement_restore_state not in ALL_PANEL_PLACEMENT_RESTORE_STATES:
            raise ValueError(
                "panel_placement_restore_state must be one of "
                f"{ALL_PANEL_PLACEMENT_RESTORE_STATES}, "
                f"got {self.panel_placement_restore_state!r}."
            )

        if self.panel_placement_restore_class not in ALL_PANEL_PLACEMENT_RESTORE_CLASSES:
            raise ValueError(
                "panel_placement_restore_class must be one of "
                f"{ALL_PANEL_PLACEMENT_RESTORE_CLASSES}, "
                f"got {self.panel_placement_restore_class!r}."
            )

        if not self.dashboard_session_restore_ready:
            raise ValueError(
                "dashboard_session_restore_ready must remain true for canonical "
                "panel placement restore entries."
            )

        if not self.display_assignment_restore_ready:
            raise ValueError(
                "display_assignment_restore_ready must remain true for canonical "
                "panel placement restore entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical "
                "panel placement restore entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical "
                "panel placement restore entries."
            )


@dataclass(frozen=True, slots=True)
class PanelPlacementRestoreContract:
    """Canonical panel placement restore contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[PanelPlacementRestoreEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical panel placement restore contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.panel_placement_restore_state
            == "panel_placement_restore_ready"
        ):
            raise ValueError(
                "ready_entries must match panel_placement_restore_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )

        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_panel_placement_restore_contract() -> PanelPlacementRestoreContract:
    """Build canonical panel placement restore contract."""
    dashboard_session_restore_contract = build_dashboard_session_restore_contract()
    display_assignment_restore_contract = build_display_assignment_restore_contract()

    dashboard_session_restore_entry = dashboard_session_restore_contract.entries[0]

    entries = (
        PanelPlacementRestoreEntry(
            panel_placement_restore_id="panel_placement_restore_001",
            workspace_id=dashboard_session_restore_entry.workspace_id,
            panel_placement_restore_state="panel_placement_restore_ready",
            panel_placement_restore_class="dashboard_panel_placement_restore",
            dashboard_session_restore_ready=True,
            display_assignment_restore_ready=bool(display_assignment_restore_contract),
            operator_visible=True,
            truth_bound=True,
            description=(
                "Canonical panel placement restore entry built from dashboard "
                "session restore and display assignment restore."
            ),
        ),
    )

    return PanelPlacementRestoreContract(
        contract_id="panel_placement_restore_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.panel_placement_restore_state
            == "panel_placement_restore_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
