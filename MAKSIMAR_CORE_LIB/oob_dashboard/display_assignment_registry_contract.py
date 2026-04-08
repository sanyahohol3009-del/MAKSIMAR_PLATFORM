from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    build_main_operator_interaction_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_action_queue_panel_contract import (
    build_operator_action_queue_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_queue_panel_contract import (
    build_operator_approval_queue_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_timeline_panel_contract import (
    build_operator_audit_timeline_panel_contract,
)


DisplayAssignmentRole = Literal[
    "primary_operator_surface",
    "secondary_operator_panel",
    "diagnostics_timeline_panel",
]

DisplayAssignmentState = Literal[
    "display_assignment_active",
]

ALL_DISPLAY_ASSIGNMENT_ROLES: tuple[DisplayAssignmentRole, ...] = (
    "primary_operator_surface",
    "secondary_operator_panel",
    "diagnostics_timeline_panel",
)

ALL_DISPLAY_ASSIGNMENT_STATES: tuple[DisplayAssignmentState, ...] = (
    "display_assignment_active",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayAssignmentRegistryEntry:
    """Canonical display assignment registry entry."""

    assignment_id: str
    display_target_id: str
    panel_or_surface_id: str
    assignment_role: DisplayAssignmentRole
    assignment_state: DisplayAssignmentState
    workspace_id: str
    replaceable: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display assignment registry entry."""
        _require_non_empty(self.assignment_id, "assignment_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.panel_or_surface_id, "panel_or_surface_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.assignment_role not in ALL_DISPLAY_ASSIGNMENT_ROLES:
            raise ValueError(
                "assignment_role must be one of "
                f"{ALL_DISPLAY_ASSIGNMENT_ROLES}, got {self.assignment_role!r}."
            )

        if self.assignment_state not in ALL_DISPLAY_ASSIGNMENT_STATES:
            raise ValueError(
                "assignment_state must be one of "
                f"{ALL_DISPLAY_ASSIGNMENT_STATES}, got {self.assignment_state!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical display assignments."
            )


@dataclass(frozen=True, slots=True)
class DisplayAssignmentRegistryContract:
    """Canonical display assignment registry contract."""

    contract_id: str
    total_entries: int
    active_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayAssignmentRegistryEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display assignment registry contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.active_entries != sum(
            1
            for entry in self.entries
            if entry.assignment_state == "display_assignment_active"
        ):
            raise ValueError("active_entries must match active assignment count.")

        if self.replaceable_entries != sum(
            1 for entry in self.entries if entry.replaceable
        ):
            raise ValueError(
                "replaceable_entries must match replaceable assignment count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_assignment_registry_contract() -> DisplayAssignmentRegistryContract:
    """Build canonical display assignment registry contract."""
    interaction_surface_contract = build_main_operator_interaction_surface_contract()
    action_queue_contract = build_operator_action_queue_panel_contract()
    approval_queue_contract = build_operator_approval_queue_panel_contract()
    audit_timeline_contract = build_operator_audit_timeline_panel_contract()

    interaction_surface_entry = interaction_surface_contract.entries[0]
    action_queue_entry = action_queue_contract.entries[0]
    approval_queue_entry = approval_queue_contract.entries[0]
    audit_timeline_entry = audit_timeline_contract.entries[0]

    entries = (
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_001",
            display_target_id="display_primary_operator",
            panel_or_surface_id=interaction_surface_entry.interaction_surface_id,
            assignment_role="primary_operator_surface",
            assignment_state="display_assignment_active",
            workspace_id=interaction_surface_entry.workspace_id,
            replaceable=False,
            operator_visible=True,
            description=(
                "Canonical primary display assignment for the main operator interaction surface."
            ),
        ),
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_002",
            display_target_id="display_secondary_diagnostics",
            panel_or_surface_id=action_queue_entry.panel_id,
            assignment_role="secondary_operator_panel",
            assignment_state="display_assignment_active",
            workspace_id=action_queue_entry.workspace_id,
            replaceable=True,
            operator_visible=True,
            description=(
                "Canonical secondary display assignment for the operator action queue panel."
            ),
        ),
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_003",
            display_target_id="display_secondary_diagnostics",
            panel_or_surface_id=approval_queue_entry.panel_id,
            assignment_role="secondary_operator_panel",
            assignment_state="display_assignment_active",
            workspace_id=approval_queue_entry.workspace_id,
            replaceable=True,
            operator_visible=True,
            description=(
                "Canonical secondary display assignment for the operator approval queue panel."
            ),
        ),
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_004",
            display_target_id="display_tertiary_expansion",
            panel_or_surface_id=audit_timeline_entry.panel_id,
            assignment_role="diagnostics_timeline_panel",
            assignment_state="display_assignment_active",
            workspace_id=audit_timeline_entry.workspace_id,
            replaceable=True,
            operator_visible=True,
            description=(
                "Canonical tertiary display assignment for the operator audit timeline panel."
            ),
        ),
    )

    return DisplayAssignmentRegistryContract(
        contract_id="display_assignment_registry_contract_001",
        total_entries=len(entries),
        active_entries=sum(
            1
            for entry in entries
            if entry.assignment_state == "display_assignment_active"
        ),
        replaceable_entries=sum(1 for entry in entries if entry.replaceable),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
