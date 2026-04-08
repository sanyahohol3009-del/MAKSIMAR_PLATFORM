from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    build_operator_intent_model,
)


ApprovalRequirement = Literal[
    "no_approval_required",
    "human_approval_required",
    "multi_factor_approval_required",
    "hardware_key_required",
]

PolicyDecisionStatus = Literal[
    "allowed",
    "blocked",
    "pending_approval",
    "deferred",
]

PolicyReasonCode = Literal[
    "read_only_surface",
    "operator_surface_allowed",
    "approval_required",
    "restricted_panel",
    "forbidden_direct_execution",
    "unknown_action",
    "policy_hold",
]

ALL_APPROVAL_REQUIREMENTS: tuple[ApprovalRequirement, ...] = (
    "no_approval_required",
    "human_approval_required",
    "multi_factor_approval_required",
    "hardware_key_required",
)

ALL_POLICY_DECISION_STATUSES: tuple[PolicyDecisionStatus, ...] = (
    "allowed",
    "blocked",
    "pending_approval",
    "deferred",
)

ALL_POLICY_REASON_CODES: tuple[PolicyReasonCode, ...] = (
    "read_only_surface",
    "operator_surface_allowed",
    "approval_required",
    "restricted_panel",
    "forbidden_direct_execution",
    "unknown_action",
    "policy_hold",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorApprovalDecisionEntry:
    """Canonical operator approval decision entry."""

    approval_decision_id: str
    operator_intent_id: str
    policy_decision_status: PolicyDecisionStatus
    approval_requirement: ApprovalRequirement
    reason_code: PolicyReasonCode
    executable_after_approval: bool
    explanation_visible_to_operator: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator approval decision entry fields."""
        _require_non_empty(self.approval_decision_id, "approval_decision_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.policy_decision_status not in ALL_POLICY_DECISION_STATUSES:
            raise ValueError(
                "policy_decision_status must be one of "
                f"{ALL_POLICY_DECISION_STATUSES}, got {self.policy_decision_status!r}."
            )

        if self.approval_requirement not in ALL_APPROVAL_REQUIREMENTS:
            raise ValueError(
                "approval_requirement must be one of "
                f"{ALL_APPROVAL_REQUIREMENTS}, got {self.approval_requirement!r}."
            )

        if self.reason_code not in ALL_POLICY_REASON_CODES:
            raise ValueError(
                f"reason_code must be one of {ALL_POLICY_REASON_CODES}, "
                f"got {self.reason_code!r}."
            )

        if self.policy_decision_status == "allowed" and self.approval_requirement != "no_approval_required":
            raise ValueError(
                "Allowed decisions must use no_approval_required."
            )

        if self.policy_decision_status == "blocked" and self.executable_after_approval:
            raise ValueError(
                "Blocked decisions cannot remain executable_after_approval."
            )

        if self.policy_decision_status == "pending_approval" and self.approval_requirement == "no_approval_required":
            raise ValueError(
                "Pending approval decisions must require an approval mode."
            )


@dataclass(frozen=True, slots=True)
class OperatorApprovalDecisionModel:
    """Canonical operator approval decision model."""

    model_id: str
    total_entries: int
    allowed_entries: int
    blocked_entries: int
    pending_approval_entries: int
    deferred_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorApprovalDecisionEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator approval decision model fields."""
        _require_non_empty(self.model_id, "model_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the model."
            )

        if self.allowed_entries != sum(
            1 for entry in self.entries if entry.policy_decision_status == "allowed"
        ):
            raise ValueError("allowed_entries must match allowed decision count.")

        if self.blocked_entries != sum(
            1 for entry in self.entries if entry.policy_decision_status == "blocked"
        ):
            raise ValueError("blocked_entries must match blocked decision count.")

        if self.pending_approval_entries != sum(
            1
            for entry in self.entries
            if entry.policy_decision_status == "pending_approval"
        ):
            raise ValueError(
                "pending_approval_entries must match pending approval decision count."
            )

        if self.deferred_entries != sum(
            1 for entry in self.entries if entry.policy_decision_status == "deferred"
        ):
            raise ValueError("deferred_entries must match deferred decision count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.explanation_visible_to_operator
        ):
            raise ValueError(
                "operator_visible_entries must match visible explanation count."
            )


def build_operator_approval_decision_model() -> OperatorApprovalDecisionModel:
    """Build canonical operator approval decision model."""
    intent_model = build_operator_intent_model()
    intent_entries = {entry.operator_intent_id: entry for entry in intent_model.entries}

    entries = (
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_001",
            operator_intent_id="operator_intent_001",
            policy_decision_status="allowed",
            approval_requirement="no_approval_required",
            reason_code="operator_surface_allowed",
            executable_after_approval=False,
            explanation_visible_to_operator=True,
            trace_id=intent_entries["operator_intent_001"].trace_id,
            description=(
                "Canonical approval decision for a view-only operator intent "
                "that remains visible and non-executing."
            ),
        ),
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_002",
            operator_intent_id="operator_intent_002",
            policy_decision_status="allowed",
            approval_requirement="no_approval_required",
            reason_code="operator_surface_allowed",
            executable_after_approval=False,
            explanation_visible_to_operator=True,
            trace_id=intent_entries["operator_intent_002"].trace_id,
            description=(
                "Canonical approval decision for a navigation operator intent "
                "that remains operator-visible and non-direct-executing."
            ),
        ),
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_003",
            operator_intent_id="operator_intent_003",
            policy_decision_status="pending_approval",
            approval_requirement="human_approval_required",
            reason_code="approval_required",
            executable_after_approval=True,
            explanation_visible_to_operator=True,
            trace_id=intent_entries["operator_intent_003"].trace_id,
            description=(
                "Canonical approval decision for a control-bound operator intent "
                "that requires explicit human approval before any handoff."
            ),
        ),
    )

    return OperatorApprovalDecisionModel(
        model_id="operator_approval_decision_model_001",
        total_entries=len(entries),
        allowed_entries=sum(
            1 for entry in entries if entry.policy_decision_status == "allowed"
        ),
        blocked_entries=sum(
            1 for entry in entries if entry.policy_decision_status == "blocked"
        ),
        pending_approval_entries=sum(
            1 for entry in entries if entry.policy_decision_status == "pending_approval"
        ),
        deferred_entries=sum(
            1 for entry in entries if entry.policy_decision_status == "deferred"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.explanation_visible_to_operator
        ),
        entries=entries,
    )
