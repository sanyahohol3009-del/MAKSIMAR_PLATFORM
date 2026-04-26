from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_guard_models import (
    OperatorInteractionGuardContract,
    OperatorInteractionGuardEntry,
)


def test_operator_interaction_guard_entry_smoke() -> None:
    entry = OperatorInteractionGuardEntry(
        dashboard_id="main_operator_dashboard",
        interaction_surface_id="main_operator_interaction_surface",
        guard_mode="guarded_operator_interaction",
        direct_execution_allowed=False,
        approval_required=True,
        policy_gate_required=True,
        forbidden_state_visible=True,
        description="Guard description.",
    )

    assert entry.dashboard_id == "main_operator_dashboard"


def test_operator_interaction_guard_entry_rejects_direct_execution() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed must be False"):
        OperatorInteractionGuardEntry(
            dashboard_id="main_operator_dashboard",
            interaction_surface_id="main_operator_interaction_surface",
            guard_mode="guarded_operator_interaction",
            direct_execution_allowed=True,
            approval_required=True,
            policy_gate_required=True,
            forbidden_state_visible=True,
            description="Guard description.",
        )


def test_operator_interaction_guard_contract_rejects_duplicates() -> None:
    entry_a = OperatorInteractionGuardEntry(
        dashboard_id="main_operator_dashboard",
        interaction_surface_id="main_operator_interaction_surface",
        guard_mode="guarded_operator_interaction",
        direct_execution_allowed=False,
        approval_required=True,
        policy_gate_required=True,
        forbidden_state_visible=True,
        description="A",
    )
    entry_b = OperatorInteractionGuardEntry(
        dashboard_id="main_operator_dashboard",
        interaction_surface_id="main_operator_interaction_surface",
        guard_mode="guarded_operator_interaction",
        direct_execution_allowed=False,
        approval_required=True,
        policy_gate_required=True,
        forbidden_state_visible=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate dashboard_id detected"):
        OperatorInteractionGuardContract(entries=(entry_a, entry_b))
