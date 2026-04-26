from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_contract import (
    build_operator_audit_visibility_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_contract import (
    build_operator_control_plane_handoff_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_models import (
    OperatorInteractionReadModelContract,
    OperatorInteractionReadModelEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_contract import (
    build_operator_intent_contract,
)


def normalize_dashboard_id(dashboard_id: str) -> str:
    """Normalize legacy and canonical dashboard identifiers."""
    mapping: dict[str, str] = {
        "dashboard_main_operator_001": "main_operator_dashboard",
        "main_operator_dashboard": "main_operator_dashboard",
    }

    if dashboard_id not in mapping:
        raise ValueError(f"unsupported dashboard_id: {dashboard_id}")

    return mapping[dashboard_id]


def build_operator_interaction_read_model_contract() -> (
    OperatorInteractionReadModelContract
):
    """Build canonical operator interaction read-model contract.

    This read model is derived from:
    - operator intent truth
    - operator control-plane handoff truth
    - operator audit visibility truth

    It remains non-executing and operator-visible.
    """
    intent_contract = build_operator_intent_contract()
    handoff_contract = build_operator_control_plane_handoff_contract()
    audit_contract = build_operator_audit_visibility_contract()

    handoff_by_dashboard = {
        entry.dashboard_id: entry for entry in handoff_contract.entries
    }
    audit_by_dashboard = {
        entry.dashboard_id: entry for entry in audit_contract.entries
    }

    entries = tuple(
        OperatorInteractionReadModelEntry(
            operator_intent_id=intent_entry.operator_intent_id,
            dashboard_id=normalize_dashboard_id(intent_entry.dashboard_id),
            workspace_id=intent_entry.workspace_id,
            interaction_lane=(
                "approval_bound_lane"
                if intent_entry.approval_required
                else "read_only_lane"
            ),
            interaction_surface_state=(
                "approval_bound_interaction_surface"
                if intent_entry.approval_required
                else "read_only_interaction_surface"
            ),
            intent_kind=intent_entry.intent_kind,
            approval_state=(
                "approval_required"
                if intent_entry.approval_required
                else "approval_not_required"
            ),
            handoff_state=(
                "handoff_ready"
                if handoff_by_dashboard[
                    normalize_dashboard_id(intent_entry.dashboard_id)
                ].action_submission_allowed
                else "handoff_blocked"
            ),
            audit_visibility_state=(
                "audit_visible_with_policy_and_approval"
                if (
                    audit_by_dashboard[
                        normalize_dashboard_id(intent_entry.dashboard_id)
                    ].policy_visibility_required
                    and audit_by_dashboard[
                        normalize_dashboard_id(intent_entry.dashboard_id)
                    ].approval_visibility_required
                )
                else "audit_visibility_incomplete"
            ),
            approval_required=intent_entry.approval_required,
            handoff_ready=(
                handoff_by_dashboard[
                    normalize_dashboard_id(intent_entry.dashboard_id)
                ].action_submission_allowed
            ),
            operator_visible=True,
            trace_id=intent_entry.trace_id,
            description=(
                "Canonical operator interaction read-model entry for "
                f"{intent_entry.operator_intent_id}."
            ),
        )
        for intent_entry in intent_contract.entries
    )

    return OperatorInteractionReadModelContract(
        contract_id="operator_interaction_read_model_contract_001",
        total_entries=len(entries),
        read_only_lane_entries=sum(
            1 for entry in entries if entry.interaction_lane == "read_only_lane"
        ),
        approval_bound_lane_entries=sum(
            1
            for entry in entries
            if entry.interaction_lane == "approval_bound_lane"
        ),
        approval_required_entries=sum(
            1 for entry in entries if entry.approval_required
        ),
        handoff_ready_entries=sum(
            1 for entry in entries if entry.handoff_ready
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
