from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_models import (
    OperatorControlPlaneHandoffContract,
    OperatorControlPlaneHandoffEntry,
)


def test_operator_control_plane_handoff_entry_smoke() -> None:
    entry = OperatorControlPlaneHandoffEntry(
        dashboard_id="main_operator_dashboard",
        interaction_surface_id="main_operator_interaction_surface",
        handoff_target="control_plane_operator_gateway",
        handoff_mode="guarded_submission_only",
        action_submission_allowed=True,
        direct_execution_allowed=False,
        approval_required=True,
        policy_gate_required=True,
        description="Handoff description.",
    )

    assert entry.dashboard_id == "main_operator_dashboard"


def test_operator_control_plane_handoff_entry_rejects_direct_execution() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        OperatorControlPlaneHandoffEntry(
            dashboard_id="main_operator_dashboard",
            interaction_surface_id="main_operator_interaction_surface",
            handoff_target="control_plane_operator_gateway",
            handoff_mode="guarded_submission_only",
            action_submission_allowed=True,
            direct_execution_allowed=True,
            approval_required=True,
            policy_gate_required=True,
            description="Handoff description.",
        )


def test_operator_control_plane_handoff_contract_rejects_duplicates() -> None:
    entry_a = OperatorControlPlaneHandoffEntry(
        dashboard_id="main_operator_dashboard",
        interaction_surface_id="main_operator_interaction_surface",
        handoff_target="control_plane_operator_gateway",
        handoff_mode="guarded_submission_only",
        action_submission_allowed=True,
        direct_execution_allowed=False,
        approval_required=True,
        policy_gate_required=True,
        description="A",
    )
    entry_b = OperatorControlPlaneHandoffEntry(
        dashboard_id="main_operator_dashboard",
        interaction_surface_id="main_operator_interaction_surface",
        handoff_target="control_plane_operator_gateway",
        handoff_mode="guarded_submission_only",
        action_submission_allowed=True,
        direct_execution_allowed=False,
        approval_required=True,
        policy_gate_required=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate dashboard_id detected"):
        OperatorControlPlaneHandoffContract(entries=(entry_a, entry_b))
