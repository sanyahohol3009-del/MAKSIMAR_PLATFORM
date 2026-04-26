from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_models import (
    MainOperatorInteractionSurfaceContract,
    MainOperatorInteractionSurfaceEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_contract import (
    build_operator_audit_visibility_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_contract import (
    build_operator_control_plane_handoff_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_contract import (
    build_operator_interaction_read_model_contract,
)


def build_main_operator_interaction_surface_contract() -> (
    MainOperatorInteractionSurfaceContract
):
    """Build canonical main-operator interaction surface contract."""
    read_model_contract = build_operator_interaction_read_model_contract()
    handoff_contract = build_operator_control_plane_handoff_contract()
    audit_contract = build_operator_audit_visibility_contract()

    handoff_by_dashboard = {
        entry.dashboard_id: entry for entry in handoff_contract.entries
    }
    audit_by_dashboard = {
        entry.dashboard_id: entry for entry in audit_contract.entries
    }

    entries = tuple(
        MainOperatorInteractionSurfaceEntry(
            interaction_surface_id=(
                f"main_operator_interaction_surface_{index:03d}"
            ),
            operator_intent_id=entry.operator_intent_id,
            dashboard_id=entry.dashboard_id,
            workspace_id=entry.workspace_id,
            surface_state="interaction_surface_ready",
            surface_class=(
                "approval_bound_surface"
                if entry.approval_required
                else "read_only_surface"
            ),
            intent_kind=entry.intent_kind,
            action_visible=True,
            disabled_state_visible=True,
            forbidden_state_visible=(
                handoff_by_dashboard[entry.dashboard_id].policy_gate_required
            ),
            pending_approval_visible=entry.approval_required,
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            audit_visible=(
                audit_by_dashboard[entry.dashboard_id].policy_visibility_required
                and audit_by_dashboard[entry.dashboard_id].approval_visibility_required
            ),
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical main operator interaction surface entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(read_model_contract.entries, start=1)
    )

    return MainOperatorInteractionSurfaceContract(
        contract_id="main_operator_interaction_surface_contract_001",
        total_entries=len(entries),
        read_only_surface_entries=sum(
            1 for entry in entries if entry.surface_class == "read_only_surface"
        ),
        approval_bound_surface_entries=sum(
            1
            for entry in entries
            if entry.surface_class == "approval_bound_surface"
        ),
        pending_approval_visible_entries=sum(
            1 for entry in entries if entry.pending_approval_visible
        ),
        handoff_ready_entries=sum(1 for entry in entries if entry.handoff_ready),
        audit_visible_entries=sum(1 for entry in entries if entry.audit_visible),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
