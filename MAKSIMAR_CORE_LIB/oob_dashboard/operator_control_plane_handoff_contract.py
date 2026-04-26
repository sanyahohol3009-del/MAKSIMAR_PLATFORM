from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_models import (
    OperatorControlPlaneHandoffContract,
    OperatorControlPlaneHandoffEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_guard_contract import (
    build_operator_interaction_guard_contract,
)


def build_operator_control_plane_handoff_contract() -> (
    OperatorControlPlaneHandoffContract
):
    """Build the canonical operator-control-plane handoff contract."""
    dashboard_contract = build_main_operator_dashboard_contract()
    guard_contract = build_operator_interaction_guard_contract()

    guard_map = {entry.dashboard_id: entry for entry in guard_contract.entries}

    entries = tuple(
        OperatorControlPlaneHandoffEntry(
            dashboard_id=entry.dashboard_id,
            interaction_surface_id=guard_map[entry.dashboard_id].interaction_surface_id,
            handoff_target="control_plane_operator_gateway",
            handoff_mode="guarded_submission_only",
            action_submission_allowed=True,
            direct_execution_allowed=False,
            approval_required=guard_map[entry.dashboard_id].approval_required,
            policy_gate_required=guard_map[entry.dashboard_id].policy_gate_required,
            description=(
                "Canonical operator handoff into the control plane. Operator actions "
                "may be submitted for downstream handling, but cannot execute directly "
                "without policy and approval."
            ),
        )
        for entry in dashboard_contract.entries
    )

    return OperatorControlPlaneHandoffContract(entries=entries)
