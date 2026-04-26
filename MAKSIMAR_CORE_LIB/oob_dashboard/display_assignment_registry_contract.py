from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


DisplayAssignmentRole = Literal[
    "foundation_primary_surface",
    "foundation_secondary_surface",
    "operator_interaction_surface",
]
DisplayAssignmentState = Literal[
    "display_assignment_active",
]

ALL_DISPLAY_ASSIGNMENT_ROLES: tuple[DisplayAssignmentRole, ...] = (
    "foundation_primary_surface",
    "foundation_secondary_surface",
    "operator_interaction_surface",
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
                f"{ALL_DISPLAY_ASSIGNMENT_ROLES}, "
                f"got {self.assignment_role!r}."
            )

        if self.assignment_state not in ALL_DISPLAY_ASSIGNMENT_STATES:
            raise ValueError(
                "assignment_state must be one of "
                f"{ALL_DISPLAY_ASSIGNMENT_STATES}, "
                f"got {self.assignment_state!r}."
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


def _resolve_workspace_ids() -> tuple[str, str]:
    """Resolve canonical foundation and operator workspace ids."""
    workspace_registry_contract = build_workspace_registry_contract()

    foundation_workspace_id: str | None = None
    operator_workspace_id: str | None = None

    for entry in workspace_registry_contract.entries:
        if entry.workspace_role == "foundation_monitoring":
            foundation_workspace_id = entry.workspace_id
        elif entry.workspace_role == "operator_interaction":
            operator_workspace_id = entry.workspace_id

    if foundation_workspace_id is None:
        raise ValueError(
            "foundation_monitoring workspace is missing from workspace registry."
        )

    if operator_workspace_id is None:
        raise ValueError(
            "operator_interaction workspace is missing from workspace registry."
        )

    return foundation_workspace_id, operator_workspace_id


def build_display_assignment_registry_contract() -> (
    DisplayAssignmentRegistryContract
):
    """Build canonical display assignment registry contract.

    This canonical version is normalized to the current display target vocabulary:
    - display_foundation_primary
    - display_foundation_secondary
    - display_operator_interaction

    It preserves the original registry semantics:
    - explicit assignment entries
    - explicit assignment roles
    - active/replaceable/operator-visible aggregates
    """
    display_target_contract = build_display_target_vocabulary_contract()
    foundation_workspace_id, operator_workspace_id = _resolve_workspace_ids()

    display_target_ids = {
        entry.display_target_id for entry in display_target_contract.entries
    }
    required_display_targets = (
        "display_foundation_primary",
        "display_foundation_secondary",
        "display_operator_interaction",
    )

    for display_target_id in required_display_targets:
        if display_target_id not in display_target_ids:
            raise ValueError(
                f"Required display target {display_target_id!r} is missing "
                "from display_target_vocabulary_contract."
            )

    entries = (
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_001",
            display_target_id="display_foundation_primary",
            panel_or_surface_id="workspace_foundation_monitoring_surface",
            assignment_role="foundation_primary_surface",
            assignment_state="display_assignment_active",
            workspace_id=foundation_workspace_id,
            replaceable=False,
            operator_visible=True,
            description=(
                "Canonical primary display assignment for the foundation "
                "monitoring workspace surface."
            ),
        ),
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_002",
            display_target_id="display_foundation_secondary",
            panel_or_surface_id="panel_logs_surface",
            assignment_role="foundation_secondary_surface",
            assignment_state="display_assignment_active",
            workspace_id=foundation_workspace_id,
            replaceable=True,
            operator_visible=True,
            description=(
                "Canonical secondary display assignment for the logs panel surface."
            ),
        ),
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_003",
            display_target_id="display_foundation_secondary",
            panel_or_surface_id="panel_topology_surface",
            assignment_role="foundation_secondary_surface",
            assignment_state="display_assignment_active",
            workspace_id=foundation_workspace_id,
            replaceable=True,
            operator_visible=True,
            description=(
                "Canonical secondary display assignment for the topology panel surface."
            ),
        ),
        DisplayAssignmentRegistryEntry(
            assignment_id="display_assignment_004",
            display_target_id="display_operator_interaction",
            panel_or_surface_id="workspace_operator_interaction_surface",
            assignment_role="operator_interaction_surface",
            assignment_state="display_assignment_active",
            workspace_id=operator_workspace_id,
            replaceable=True,
            operator_visible=True,
            description=(
                "Canonical operator interaction display assignment for the "
                "operator interaction workspace surface."
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
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
