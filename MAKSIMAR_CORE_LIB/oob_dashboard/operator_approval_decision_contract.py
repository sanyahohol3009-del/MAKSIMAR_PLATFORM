from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_decision_models import (
    build_operator_approval_decision_model,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    build_operator_intent_model,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_vocabulary_contract import (
    build_operator_intent_vocabulary_contract,
)


@dataclass(frozen=True, slots=True)
class OperatorApprovalDecisionContractEntry:
    """Canonical operator approval decision contract entry."""

    approval_decision_id: str
    operator_intent_id: str
    policy_decision_status: str
    approval_requirement: str
    reason_code: str
    executable_after_approval: bool
    explanation_visible_to_operator: bool
    intent_registered: bool
    policy_status_registered: bool
    approval_requirement_registered: bool
    reason_code_registered: bool
    structurally_valid: bool
    trace_id: str
    description: str


@dataclass(frozen=True, slots=True)
class OperatorApprovalDecisionContract:
    """Canonical operator approval decision contract."""

    contract_id: str
    total_entries: int
    structurally_valid_entries: int
    allowed_entries: int
    blocked_entries: int
    pending_approval_entries: int
    deferred_entries: int
    executable_after_approval_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorApprovalDecisionContractEntry, ...]


def build_operator_approval_decision_contract() -> OperatorApprovalDecisionContract:
    """Build canonical operator approval decision contract."""
    decision_model = build_operator_approval_decision_model()
    intent_model = build_operator_intent_model()
    vocabulary_contract = build_operator_intent_vocabulary_contract()

    registered_intent_ids = {
        entry.operator_intent_id for entry in intent_model.entries
    }
    registered_policy_statuses = {
        entry.canonical_value
        for entry in vocabulary_contract.entries
        if entry.vocabulary_group == "intent_state"
    }
    registered_approval_requirements = {
        "no_approval_required",
        "human_approval_required",
        "multi_factor_approval_required",
        "hardware_key_required",
    }
    registered_reason_codes = {
        "read_only_surface",
        "operator_surface_allowed",
        "approval_required",
        "restricted_panel",
        "forbidden_direct_execution",
        "unknown_action",
        "policy_hold",
    }

    status_map = {
        "allowed": "intent_validated",
        "blocked": "intent_blocked",
        "pending_approval": "intent_pending_approval",
        "deferred": "intent_created",
    }

    entries = tuple(
        OperatorApprovalDecisionContractEntry(
            approval_decision_id=entry.approval_decision_id,
            operator_intent_id=entry.operator_intent_id,
            policy_decision_status=entry.policy_decision_status,
            approval_requirement=entry.approval_requirement,
            reason_code=entry.reason_code,
            executable_after_approval=entry.executable_after_approval,
            explanation_visible_to_operator=entry.explanation_visible_to_operator,
            intent_registered=entry.operator_intent_id in registered_intent_ids,
            policy_status_registered=(
                status_map[entry.policy_decision_status] in registered_policy_statuses
            ),
            approval_requirement_registered=(
                entry.approval_requirement in registered_approval_requirements
            ),
            reason_code_registered=entry.reason_code in registered_reason_codes,
            structurally_valid=(
                entry.operator_intent_id in registered_intent_ids
                and status_map[entry.policy_decision_status] in registered_policy_statuses
                and entry.approval_requirement in registered_approval_requirements
                and entry.reason_code in registered_reason_codes
            ),
            trace_id=entry.trace_id,
            description=entry.description,
        )
        for entry in decision_model.entries
    )

    return OperatorApprovalDecisionContract(
        contract_id="operator_approval_decision_contract_001",
        total_entries=len(entries),
        structurally_valid_entries=sum(
            1 for entry in entries if entry.structurally_valid
        ),
        allowed_entries=sum(
            1 for entry in entries if entry.policy_decision_status == "allowed"
        ),
        blocked_entries=sum(
            1 for entry in entries if entry.policy_decision_status == "blocked"
        ),
        pending_approval_entries=sum(
            1
            for entry in entries
            if entry.policy_decision_status == "pending_approval"
        ),
        deferred_entries=sum(
            1 for entry in entries if entry.policy_decision_status == "deferred"
        ),
        executable_after_approval_entries=sum(
            1 for entry in entries if entry.executable_after_approval
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.explanation_visible_to_operator
        ),
        entries=entries,
    )
