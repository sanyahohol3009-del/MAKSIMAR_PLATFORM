from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import build_node_memory_scope_contract


def test_dev_home_mobile_scope_split_smoke() -> None:
    contract = build_node_memory_scope_contract()

    roles = {entry.node_role for entry in contract.entries}
    node_ids = {entry.node_id for entry in contract.entries}
    memory_map_ids = {entry.memory_map_id for entry in contract.entries}

    assert roles == {"DEV_NODE", "HOME_NODE", "MOBILE_NODE"}
    assert node_ids == {"dev_node_001", "home_node_001", "mobile_node_001"}
    assert memory_map_ids == {"memory_map_global_001"}
