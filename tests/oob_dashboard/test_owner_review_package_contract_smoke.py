from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.owner_review_package_contract import (
    build_owner_review_package_contract,
)


def test_owner_review_package_contract_builds() -> None:
    """Owner review package contract should build successfully."""
    contract = build_owner_review_package_contract()

    assert contract.contract_id == "owner_review_package_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_review_entries == 2
    assert contract.approval_bound_review_entries == 1
    assert contract.audit_visible_entries == 3
    assert contract.operator_visible_entries == 3


def test_owner_review_package_contract_contains_expected_entries() -> None:
    """Owner review package contract should contain expected canonical entries."""
    contract = build_owner_review_package_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert (
        entry_map["operator_intent_001"].owner_review_package_class
        == "read_only_review_package"
    )
    assert (
        entry_map["operator_intent_001"].owner_review_evidence_mode
        == "preview_and_audit_evidence"
    )
    assert entry_map["operator_intent_001"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_002"].owner_review_package_class
        == "read_only_review_package"
    )
    assert entry_map["operator_intent_002"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_003"].owner_review_package_class
        == "approval_bound_review_package"
    )
    assert (
        entry_map["operator_intent_003"].owner_review_evidence_mode
        == "preview_approval_and_audit_evidence"
    )
    assert entry_map["operator_intent_003"].panel_id == "approval_queue"
