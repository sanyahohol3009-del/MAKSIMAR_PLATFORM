from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_contract import (
    build_main_operator_dashboard_read_model_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_workspace_binding_contract import (
    build_operator_workspace_binding_contract,
)


GuardDecision = Literal[
    "allowed_read_only",
    "allowed_with_approval",
    "blocked_direct_execution",
]

InteractionSurface = Literal[
    "dashboard_read_model",
    "operator_workspace_binding",
]


@dataclass(frozen=True, slots=True)
class OperatorInteractionGuardEntry:
    """Canonical operator interaction guard entry."""

    dashboard_id: str
    workspace_id: str
    interaction_surface: InteractionSurface
    guard_decision: GuardDecision
    direct_execution_allowed: bool
    approval_required_for_mutation: bool
    description: str


@dataclass(frozen=True, slots=True)
class OperatorInteractionGuardContract:
    """Canonical operator interaction guard contract."""

    total_entries: int
    allowed_read_only_entries: int
    allowed_with_approval_entries: int
    blocked_direct_execution_entries: int
    entries: tuple[OperatorInteractionGuardEntry, ...]


def build_operator_interaction_guard_contract() -> (
    OperatorInteractionGuardContract
):
    """Build canonical operator interaction guard contract."""
    dashboard_read_model_contract = build_main_operator_dashboard_read_model_contract()
    workspace_binding_contract = build_operator_workspace_binding_contract()

    binding_map = {
        entry.workspace_id: entry for entry in workspace_binding_contract.entries
    }

    entries = tuple(
        OperatorInteractionGuardEntry(
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            interaction_surface="dashboard_read_model",
            guard_decision=(
                "allowed_with_approval"
                if binding_map[entry.workspace_id].supports_interaction
                else "allowed_read_only"
            ),
            direct_execution_allowed=False,
            approval_required_for_mutation=binding_map[
                entry.workspace_id
            ].supports_interaction,
            description=(
                f"Canonical operator interaction guard entry for {entry.workspace_id}."
            ),
        )
        for entry in dashboard_read_model_contract.entries
        if entry.workspace_id in binding_map
    )

    return OperatorInteractionGuardContract(
        total_entries=len(entries),
        allowed_read_only_entries=sum(
            1 for entry in entries if entry.guard_decision == "allowed_read_only"
        ),
        allowed_with_approval_entries=sum(
            1 for entry in entries if entry.guard_decision == "allowed_with_approval"
        ),
        blocked_direct_execution_entries=sum(
            1 for entry in entries if entry.guard_decision == "blocked_direct_execution"
        ),
        entries=entries,
    )
