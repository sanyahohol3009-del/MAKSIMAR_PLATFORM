from __future__ import annotations

from MAKSIMAR_CORE_LIB.secure_sync_update_transport import (
    build_secure_sync_update_transport_contract,
)


def test_secure_sync_update_transport_contract_builds() -> None:
    """Secure sync update transport contract should build successfully."""
    contract = build_secure_sync_update_transport_contract()

    assert contract.total_entries == 3
    assert contract.local_transport_entries == 2
    assert contract.restricted_cross_node_entries == 1
    assert contract.approval_required_entries == 1
    assert contract.defined_entries == 3


def test_secure_sync_update_transport_contract_contains_expected_dev_local_entry() -> None:
    """Secure sync transport should expose expected DEV local entry."""
    contract = build_secure_sync_update_transport_contract()
    entry = contract.entries[0]

    assert entry.secure_transport_entry_id == "transport_dev_local_001"
    assert entry.transport_class == "local_control_transport"
    assert entry.source_node_id == "dev_001"
    assert entry.target_node_id == "dev_001"
    assert entry.transport_mode == "local_same_node_transport"


def test_secure_sync_update_transport_contract_contains_expected_dev_home_entry() -> None:
    """Secure sync transport should expose expected DEV→HOME entry."""
    contract = build_secure_sync_update_transport_contract()
    entry = contract.entries[1]

    assert entry.secure_transport_entry_id == "transport_dev_home_001"
    assert entry.transport_class == "restricted_update_transport"
    assert entry.source_node_id == "dev_001"
    assert entry.target_node_id == "home_001"
    assert entry.transport_mode == "restricted_cross_node_transport"
    assert entry.approval_mode == "approval_required"


def test_secure_sync_update_transport_contract_contains_expected_mobile_local_entry() -> None:
    """Secure sync transport should expose expected MOBILE local entry."""
    contract = build_secure_sync_update_transport_contract()
    entry = contract.entries[2]

    assert entry.secure_transport_entry_id == "transport_mobile_local_001"
    assert entry.transport_class == "local_mobile_transport"
    assert entry.source_node_id == "mobile_001"
    assert entry.target_node_id == "mobile_001"
    assert entry.transport_mode == "local_same_node_transport"
