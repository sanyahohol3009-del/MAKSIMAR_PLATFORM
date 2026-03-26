from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_node_role_contract,
)


def test_node_role_contract_builds() -> None:
    """Node role contract should build successfully."""
    contract = build_node_role_contract()

    assert contract.total_nodes == 3
    assert len(contract.nodes) == 3


def test_node_role_contract_contains_mobile_dev_home() -> None:
    """Node role contract should expose mobile, dev, and home nodes."""
    contract = build_node_role_contract()

    role_types = {node.role_type for node in contract.nodes}

    assert "mobile_node" in role_types
    assert "dev_node" in role_types
    assert "home_node" in role_types
