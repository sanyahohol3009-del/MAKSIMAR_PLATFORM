from __future__ import annotations

from MAKSIMAR_CORE_LIB.multi_node_health_registry import (
    build_multi_node_health_registry_contract,
)


def test_multi_node_health_registry_contract_builds() -> None:
    """Multi-node health registry contract should build successfully."""
    contract = build_multi_node_health_registry_contract()

    assert contract.total_entries == 3
    assert contract.normal_runtime_entries == 2
    assert contract.throttled_runtime_entries == 1
    assert contract.degraded_active_entries == 1
    assert contract.registered_entries == 3


def test_multi_node_health_registry_contract_contains_expected_dev_entry() -> None:
    """Multi-node health registry should expose expected DEV entry."""
    contract = build_multi_node_health_registry_contract()
    entry = contract.entries[0]

    assert entry.health_registry_entry_id == "nodehealth_dev_001"
    assert entry.node_id == "dev_001"
    assert entry.linked_topology_entry_id == "nodetopology_dev_001"
    assert entry.health_class == "healthy_control"
    assert entry.runtime_state == "normal"
    assert entry.health_score == 96


def test_multi_node_health_registry_contract_contains_expected_home_entry() -> None:
    """Multi-node health registry should expose expected HOME entry."""
    contract = build_multi_node_health_registry_contract()
    entry = contract.entries[1]

    assert entry.health_registry_entry_id == "nodehealth_home_001"
    assert entry.node_id == "home_001"
    assert entry.linked_topology_entry_id == "nodetopology_home_001"
    assert entry.health_class == "healthy_compute"
    assert entry.runtime_state == "throttled"
    assert entry.degraded_flag_active is True


def test_multi_node_health_registry_contract_contains_expected_mobile_entry() -> None:
    """Multi-node health registry should expose expected MOBILE entry."""
    contract = build_multi_node_health_registry_contract()
    entry = contract.entries[2]

    assert entry.health_registry_entry_id == "nodehealth_mobile_001"
    assert entry.node_id == "mobile_001"
    assert entry.linked_topology_entry_id == "nodetopology_mobile_001"
    assert entry.health_class == "healthy_mobile_proxy"
    assert entry.runtime_state == "normal"
    assert entry.routing_relevance == "mobile_entry_routing"
