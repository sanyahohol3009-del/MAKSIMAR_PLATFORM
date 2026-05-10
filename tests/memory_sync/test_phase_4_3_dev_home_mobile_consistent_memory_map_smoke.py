from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import (
    build_memory_sync_phase_preview,
    build_memory_sync_preview,
    build_node_memory_scope_contract,
)


def test_phase_4_3_dev_home_mobile_consistent_memory_map_smoke() -> None:
    scopes = build_node_memory_scope_contract()
    preview = build_memory_sync_preview()
    phase_preview = build_memory_sync_phase_preview()

    assert {entry.node_role for entry in scopes.entries} == {"DEV_NODE", "HOME_NODE", "MOBILE_NODE"}
    assert {entry.memory_map_id for entry in scopes.entries} == {"memory_map_global_001"}
    assert preview["memory_map_ids"] == ("memory_map_global_001",)
    assert phase_preview["memory_map_ids"] == ("memory_map_global_001",)
