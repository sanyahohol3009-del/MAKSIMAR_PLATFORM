from __future__ import annotations

from MAKSIMAR_CORE_LIB.network_trust_boundaries import (
    build_network_trust_boundaries_contract,
)


def test_network_trust_boundaries_contract_builds() -> None:
    """Network trust boundaries contract should build successfully."""
    contract = build_network_trust_boundaries_contract()

    assert contract.total_entries == 3
    assert contract.local_zone_entries == 2
    assert contract.restricted_cross_zone_entries == 1
    assert contract.elevated_risk_entries == 1
    assert contract.defined_entries == 3


def test_network_trust_boundaries_contract_contains_expected_dev_local_entry() -> None:
    """Network trust boundaries should expose expected DEV local entry."""
    contract = build_network_trust_boundaries_contract()
    entry = contract.entries[0]

    assert entry.trust_boundary_entry_id == "trustboundary_dev_local_001"
    assert entry.source_node_id == "dev_001"
    assert entry.target_node_id == "dev_001"
    assert entry.trust_zone_class == "local_same_zone"
    assert entry.boundary_requirement == "local_only"


def test_network_trust_boundaries_contract_contains_expected_dev_home_entry() -> None:
    """Network trust boundaries should expose expected DEV→HOME entry."""
    contract = build_network_trust_boundaries_contract()
    entry = contract.entries[1]

    assert entry.trust_boundary_entry_id == "trustboundary_dev_home_001"
    assert entry.source_node_id == "dev_001"
    assert entry.target_node_id == "home_001"
    assert entry.trust_zone_class == "cross_zone_restricted"
    assert entry.boundary_risk_class == "elevated"
    assert entry.boundary_requirement == "approval_and_restricted_route"


def test_network_trust_boundaries_contract_contains_expected_mobile_local_entry() -> None:
    """Network trust boundaries should expose expected MOBILE local entry."""
    contract = build_network_trust_boundaries_contract()
    entry = contract.entries[2]

    assert entry.trust_boundary_entry_id == "trustboundary_mobile_local_001"
    assert entry.source_node_id == "mobile_001"
    assert entry.target_node_id == "mobile_001"
    assert entry.trust_zone_class == "local_same_zone"
    assert entry.boundary_requirement == "local_only"
