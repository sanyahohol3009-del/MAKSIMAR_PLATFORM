from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.view_composition_contract import (
    build_dashboard_view_composition_contract,
)


def test_view_composition_contract_builds() -> None:
    """View composition contract should build successfully."""
    contract = build_dashboard_view_composition_contract()

    assert contract.total_panels == 8
    assert len(contract.composed_panels) == 8
    assert contract.operator_visible is True


def test_view_composition_contract_uses_current_panel_set() -> None:
    """View composition contract should reflect the current canonical panel set."""
    contract = build_dashboard_view_composition_contract()

    assert contract.composed_panels == (
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
        "action_queue",
        "approval_queue",
        "audit_timeline",
    )
