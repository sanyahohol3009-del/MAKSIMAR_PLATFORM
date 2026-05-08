from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_global_registry_projection_contract,
)


def test_global_registry_unlimited_counts_smoke() -> None:
    contract = build_global_registry_projection_contract()

    assert contract.total_entries >= 1
    assert contract.total_entries == len(contract.entries)

    registry_ids = tuple(entry.registry_id for entry in contract.entries)
    assert len(set(registry_ids)) == len(registry_ids)

    kinds = {entry.entry_kind for entry in contract.entries}
    assert "module" in kinds
    assert "storage_node" in kinds
    assert "dashboard_view" in kinds
