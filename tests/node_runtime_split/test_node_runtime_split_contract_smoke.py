from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_runtime_split import (
    build_node_runtime_split_contract,
)


def test_node_runtime_split_contract_builds() -> None:
    """Node runtime split contract should build successfully."""
    contract = build_node_runtime_split_contract()

    assert contract.total_entries == 3
    assert contract.heavy_execution_nodes == 1
    assert contract.throttled_runtime_nodes == 1
    assert contract.split_valid_entries == 3


def test_node_runtime_split_contract_contains_expected_dev_entry() -> None:
    """Node runtime split should expose expected DEV_NODE entry."""
    contract = build_node_runtime_split_contract()
    entry = contract.entries[0]

    assert entry.node_id == "dev_001"
    assert entry.node_type == "DEV_NODE"
    assert entry.static_capacity_class == "medium"
    assert entry.heavy_execution_allowed is False
    assert entry.runtime_state == "open"
    assert entry.pressure_level == "normal"


def test_node_runtime_split_contract_contains_expected_home_entry() -> None:
    """Node runtime split should expose expected HOME_NODE entry."""
    contract = build_node_runtime_split_contract()
    entry = contract.entries[1]

    assert entry.node_id == "home_001"
    assert entry.node_type == "HOME_NODE"
    assert entry.static_capacity_class == "heavy"
    assert entry.heavy_execution_allowed is True
    assert entry.runtime_state == "throttled"
    assert entry.pressure_level == "elevated"


def test_node_runtime_split_contract_contains_expected_mobile_entry() -> None:
    """Node runtime split should expose expected MOBILE_NODE entry."""
    contract = build_node_runtime_split_contract()
    entry = contract.entries[2]

    assert entry.node_id == "mobile_001"
    assert entry.node_type == "MOBILE_NODE"
    assert entry.static_capacity_class == "light"
    assert entry.heavy_execution_allowed is False
    assert entry.runtime_state == "open"
    assert entry.pressure_level == "normal"


def test_node_runtime_split_contract_preserves_split_validity() -> None:
    """Node runtime split should preserve static/runtime separation validity."""
    contract = build_node_runtime_split_contract()

    for entry in contract.entries:
        assert entry.split_valid is True
        assert 0 <= entry.health_score <= 100
        assert entry.queue_depth >= 0
