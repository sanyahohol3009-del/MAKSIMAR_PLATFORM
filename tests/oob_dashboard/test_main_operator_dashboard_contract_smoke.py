from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)


def test_main_operator_dashboard_contract_builds() -> None:
    contract = build_main_operator_dashboard_contract()

    assert len(contract.entries) == 1
    assert contract.entries[0].dashboard_id == "main_operator_dashboard"


def test_main_operator_dashboard_contract_values() -> None:
    contract = build_main_operator_dashboard_contract()
    entry = contract.entries[0]

    assert entry.dashboard_role == "main_operator"
    assert entry.primary_workspace_id == "workspace_operator_interaction"
    assert entry.secondary_workspace_ids == ("workspace_foundation_monitoring",)
    assert entry.read_only_foundation_reuse is True
    assert entry.creates_second_root is False
