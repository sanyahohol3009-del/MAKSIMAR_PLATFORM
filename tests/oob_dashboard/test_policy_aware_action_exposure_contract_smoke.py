from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_policy_aware_action_exposure_contract,
)


def test_policy_aware_action_exposure_contract_builds() -> None:
    """Policy-aware action exposure contract should build successfully."""
    contract = build_policy_aware_action_exposure_contract()

    assert contract.total_entries == 1
    assert contract.read_only_exposed_entries == 0
    assert contract.approval_gated_exposed_entries == 1


def test_policy_aware_action_exposure_entry() -> None:
    """Policy-aware action exposure entry should remain canonical."""
    contract = build_policy_aware_action_exposure_contract()
    entry = contract.entries[0]

    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.action_exposure_mode == "approval_gated_exposed"
    assert entry.action_exposure_status == "visible_but_not_executed"
    assert entry.direct_execution_allowed is False
    assert entry.approval_required is True
