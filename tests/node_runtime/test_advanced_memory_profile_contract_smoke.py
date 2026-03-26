from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    build_advanced_memory_profile_contract,
)


def test_advanced_memory_profile_contract_builds() -> None:
    """Advanced memory profile contract should build successfully."""
    contract = build_advanced_memory_profile_contract()

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3


def test_advanced_memory_profile_contract_contains_memory_fields() -> None:
    """Advanced memory profile contract should expose advanced memory fields."""
    contract = build_advanced_memory_profile_contract()

    for node in contract.nodes:
        assert node.ram_total_gb >= 0
        assert node.ram_frequency_mhz >= 0
        assert node.ram_module_count >= 0
        assert node.ram_channels >= 0
        assert node.ram_layout != ""
        assert node.registered_or_buffered != ""
        assert node.slot_population != ""
