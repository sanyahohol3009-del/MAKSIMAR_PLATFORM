from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_policy_aware_action_exposure_contract,
)


def test_policy_aware_action_exposure_contract_builds() -> None:
    """Policy-aware action exposure contract should build successfully."""
    contract = build_policy_aware_action_exposure_contract()

    assert contract.total_entries == 3
    assert contract.read_only_exposed_entries == 2
    assert contract.approval_gated_exposed_entries == 1


def test_policy_aware_action_exposure_contract_contains_expected_entries() -> None:
    """Policy-aware action exposure contract should contain expected canonical entries."""
    contract = build_policy_aware_action_exposure_contract()

    read_only_entries = [
        entry
        for entry in contract.entries
        if entry.action_exposure_mode == "read_only_exposed"
    ]
    approval_gated_entries = [
        entry
        for entry in contract.entries
        if entry.action_exposure_mode == "approval_gated_exposed"
    ]

    assert len(read_only_entries) == 2
    assert len(approval_gated_entries) == 1

    for entry in contract.entries:
        assert entry.dashboard_id == "dashboard_main_operator_001"
        assert entry.workspace_id == "workspace_operator_main"
        assert entry.action_exposure_status == "visible_but_not_executed"
        assert entry.direct_execution_allowed is False

    for entry in read_only_entries:
        assert entry.approval_required is False

    approval_entry = approval_gated_entries[0]
    assert approval_entry.action_exposure_mode == "approval_gated_exposed"
    assert approval_entry.approval_required is True
