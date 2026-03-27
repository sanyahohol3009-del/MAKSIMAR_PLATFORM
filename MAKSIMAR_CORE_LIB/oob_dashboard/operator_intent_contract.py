from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_guard_contract import (
    build_operator_interaction_guard_contract,
)


IntentKind = Literal[
    "read_only_navigation",
    "guarded_operator_mutation",
]

IntentSource = Literal[
    "dashboard_operator_surface",
]

IntentStatus = Literal[
    "intent_only",
]


@dataclass(frozen=True, slots=True)
class OperatorIntentEntry:
    """Canonical operator intent entry."""

    dashboard_id: str
    workspace_id: str
    intent_kind: IntentKind
    intent_source: IntentSource
    intent_status: IntentStatus
    approval_required: bool
    direct_execution_allowed: bool
    description: str


@dataclass(frozen=True, slots=True)
class OperatorIntentContract:
    """Canonical operator intent contract."""

    total_entries: int
    read_only_navigation_entries: int
    guarded_operator_mutation_entries: int
    approval_required_entries: int
    entries: tuple[OperatorIntentEntry, ...]


def build_operator_intent_contract() -> OperatorIntentContract:
    """Build canonical operator intent contract."""
    interaction_guard_contract = build_operator_interaction_guard_contract()

    entries = tuple(
        OperatorIntentEntry(
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            intent_kind=(
                "guarded_operator_mutation"
                if entry.approval_required_for_mutation
                else "read_only_navigation"
            ),
            intent_source="dashboard_operator_surface",
            intent_status="intent_only",
            approval_required=entry.approval_required_for_mutation,
            direct_execution_allowed=entry.direct_execution_allowed,
            description=(
                f"Canonical operator intent entry for {entry.workspace_id}."
            ),
        )
        for entry in interaction_guard_contract.entries
    )

    return OperatorIntentContract(
        total_entries=len(entries),
        read_only_navigation_entries=sum(
            1 for entry in entries if entry.intent_kind == "read_only_navigation"
        ),
        guarded_operator_mutation_entries=sum(
            1
            for entry in entries
            if entry.intent_kind == "guarded_operator_mutation"
        ),
        approval_required_entries=sum(1 for entry in entries if entry.approval_required),
        entries=entries,
    )
