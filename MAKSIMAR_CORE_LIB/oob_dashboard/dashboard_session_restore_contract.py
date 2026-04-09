from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_restore_continuity_contract import (
    build_display_restore_continuity_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_restore_contract import (
    build_workspace_restore_contract,
)


DashboardSessionRestoreState = Literal[
    "dashboard_session_restore_ready",
]

DashboardSessionRestoreClass = Literal[
    "dashboard_session_restore",
]

ALL_DASHBOARD_SESSION_RESTORE_STATES: tuple[DashboardSessionRestoreState, ...] = (
    "dashboard_session_restore_ready",
)

ALL_DASHBOARD_SESSION_RESTORE_CLASSES: tuple[DashboardSessionRestoreClass, ...] = (
    "dashboard_session_restore",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DashboardSessionRestoreEntry:
    """Canonical dashboard session restore entry."""

    dashboard_session_restore_id: str
    workspace_id: str
    dashboard_session_restore_state: DashboardSessionRestoreState
    dashboard_session_restore_class: DashboardSessionRestoreClass
    workspace_restore_ready: bool
    display_restore_continuity_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical dashboard session restore entry."""
        _require_non_empty(
            self.dashboard_session_restore_id, "dashboard_session_restore_id"
        )
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.dashboard_session_restore_state not in ALL_DASHBOARD_SESSION_RESTORE_STATES:
            raise ValueError(
                "dashboard_session_restore_state must be one of "
                f"{ALL_DASHBOARD_SESSION_RESTORE_STATES}, "
                f"got {self.dashboard_session_restore_state!r}."
            )

        if self.dashboard_session_restore_class not in ALL_DASHBOARD_SESSION_RESTORE_CLASSES:
            raise ValueError(
                "dashboard_session_restore_class must be one of "
                f"{ALL_DASHBOARD_SESSION_RESTORE_CLASSES}, "
                f"got {self.dashboard_session_restore_class!r}."
            )

        if not self.workspace_restore_ready:
            raise ValueError(
                "workspace_restore_ready must remain true for canonical "
                "dashboard session restore entries."
            )

        if not self.display_restore_continuity_ready:
            raise ValueError(
                "display_restore_continuity_ready must remain true for canonical "
                "dashboard session restore entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical "
                "dashboard session restore entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical "
                "dashboard session restore entries."
            )


@dataclass(frozen=True, slots=True)
class DashboardSessionRestoreContract:
    """Canonical dashboard session restore contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[DashboardSessionRestoreEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical dashboard session restore contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.dashboard_session_restore_state
            == "dashboard_session_restore_ready"
        ):
            raise ValueError(
                "ready_entries must match dashboard_session_restore_ready count."
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


def build_dashboard_session_restore_contract() -> DashboardSessionRestoreContract:
    """Build canonical dashboard session restore contract."""
    workspace_restore_contract = build_workspace_restore_contract()
    display_restore_continuity_contract = build_display_restore_continuity_contract()

    workspace_restore_entry = workspace_restore_contract.entries[0]

    entries = (
        DashboardSessionRestoreEntry(
            dashboard_session_restore_id="dashboard_session_restore_001",
            workspace_id=workspace_restore_entry.workspace_id,
            dashboard_session_restore_state="dashboard_session_restore_ready",
            dashboard_session_restore_class="dashboard_session_restore",
            workspace_restore_ready=True,
            display_restore_continuity_ready=bool(display_restore_continuity_contract),
            operator_visible=True,
            truth_bound=True,
            description=(
                "Canonical dashboard session restore entry built from workspace "
                "restore and display restore continuity."
            ),
        ),
    )

    return DashboardSessionRestoreContract(
        contract_id="dashboard_session_restore_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.dashboard_session_restore_state
            == "dashboard_session_restore_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
