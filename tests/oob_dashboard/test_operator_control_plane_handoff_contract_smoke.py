from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_contract import (
    build_operator_control_plane_handoff_contract,
)


def test_operator_control_plane_handoff_contract_builds() -> None:
    contract = build_operator_control_plane_handoff_contract()

    assert len(contract.entries) == 1
    assert contract.entries[0].dashboard_id == "main_operator_dashboard"


def test_operator_control_plane_handoff_contract_values() -> None:
    contract = build_operator_control_plane_handoff_contract()
    entry = contract.entries[0]

    assert entry.interaction_surface_id == "main_operator_interaction_surface"
    assert entry.handoff_target == "control_plane_operator_gateway"
    assert entry.handoff_mode == "guarded_submission_only"
    assert entry.action_submission_allowed is True
    assert entry.direct_execution_allowed is False
    assert entry.approval_required is True
    assert entry.policy_gate_required is True
