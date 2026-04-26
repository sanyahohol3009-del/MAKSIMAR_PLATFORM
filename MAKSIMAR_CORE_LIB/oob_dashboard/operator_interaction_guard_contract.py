from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_guard_models import (
    OperatorInteractionGuardContract,
    OperatorInteractionGuardEntry,
)


def build_operator_interaction_guard_contract() -> OperatorInteractionGuardContract:
    """Build the canonical operator interaction guard contract."""
    dashboard_contract = build_main_operator_dashboard_contract()

    entries = tuple(
        OperatorInteractionGuardEntry(
            dashboard_id=entry.dashboard_id,
            interaction_surface_id="main_operator_interaction_surface",
            guard_mode="guarded_operator_interaction",
            direct_execution_allowed=False,
            approval_required=True,
            policy_gate_required=True,
            forbidden_state_visible=True,
            description=(
                "Canonical operator interaction guard for the main operator "
                "dashboard. Interaction remains visible, but direct execution is "
                "forbidden without policy and approval flow."
            ),
        )
        for entry in dashboard_contract.entries
    )

    return OperatorInteractionGuardContract(entries=entries)
