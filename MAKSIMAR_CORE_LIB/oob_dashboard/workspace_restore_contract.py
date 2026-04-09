from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_restore_contract import (
    build_display_assignment_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_restore_continuity_contract import (
    build_display_restore_continuity_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_read_model_contract import (
    build_workspace_read_model_contract,
)


WorkspaceRestoreState = Literal[
    "workspace_restore_ready",
]

WorkspaceRestoreClass = Literal[
    "dashboard_workspace_restore",
]

ALL_WORKSPACE_RESTORE_STATES: tuple[WorkspaceRestoreState, ...] = (
    "workspace_restore_ready",
)

ALL_WORKSPACE_RESTORE_CLASSES: tuple[WorkspaceRestoreClass, ...] = (
    "dashboard_workspace_restore",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class WorkspaceRestoreEntry:
    """Canonical workspace restore entry."""

    workspace_restore_id: str
    workspace_id: str
    workspace_restore_state: WorkspaceRestoreState
    workspace_restore_class: WorkspaceRestoreClass
    workspace_read_model_ready: bool
    display_assignment_restore_ready: bool
    display_restore_continuity_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical workspace restore entry."""
        _require_non_empty(self.workspace_restore_id, "workspace_restore_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.workspace_restore_state not in ALL_WORKSPACE_RESTORE_STATES:
            raise ValueError(
                "workspace_restore_state must be one of "
                f"{ALL_WORKSPACE_RESTORE_STATES}, "
                f"got {self.workspace_restore_state!r}."
            )

        if self.workspace_restore_class not in ALL_WORKSPACE_RESTORE_CLASSES:
            raise ValueError(
                "workspace_restore_class must be one of "
                f"{ALL_WORKSPACE_RESTORE_CLASSES}, "
                f"got {self.workspace_restore_class!r}."
            )

        if not self.workspace_read_model_ready:
            raise ValueError(
                "workspace_read_model_ready must remain true for canonical "
                "workspace restore entries."
            )

        if not self.display_assignment_restore_ready:
            raise ValueError(
                "display_assignment_restore_ready must remain true for canonical "
                "workspace restore entries."
            )

        if not self.display_restore_continuity_ready:
            raise ValueError(
                "display_restore_continuity_ready must remain true for canonical "
                "workspace restore entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical workspace restore entries."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical workspace restore entries."
            )


@dataclass(frozen=True, slots=True)
class WorkspaceRestoreContract:
    """Canonical workspace restore contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[WorkspaceRestoreEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical workspace restore contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.workspace_restore_state == "workspace_restore_ready"
        ):
            raise ValueError(
                "ready_entries must match workspace_restore_ready count."
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


def build_workspace_restore_contract() -> WorkspaceRestoreContract:
    """Build canonical workspace restore contract."""
    workspace_read_model_contract = build_workspace_read_model_contract()
    display_assignment_restore_contract = build_display_assignment_restore_contract()
    display_restore_continuity_contract = build_display_restore_continuity_contract()

    workspace_read_model_entry = workspace_read_model_contract.entries[0]

    entries = (
        WorkspaceRestoreEntry(
            workspace_restore_id="workspace_restore_001",
            workspace_id=workspace_read_model_entry.workspace_id,
            workspace_restore_state="workspace_restore_ready",
            workspace_restore_class="dashboard_workspace_restore",
            workspace_read_model_ready=True,
            display_assignment_restore_ready=bool(display_assignment_restore_contract),
            display_restore_continuity_ready=bool(display_restore_continuity_contract),
            operator_visible=True,
            truth_bound=True,
            description=(
                "Canonical workspace restore entry built from workspace read model, "
                "display assignment restore, and display restore continuity."
            ),
        ),
    )

    return WorkspaceRestoreContract(
        contract_id="workspace_restore_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.workspace_restore_state == "workspace_restore_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
