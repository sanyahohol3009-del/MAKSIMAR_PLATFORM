from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_existing_domain_inventory,
)


def test_existing_domain_inventory_smoke() -> None:
    inventory = build_existing_domain_inventory()

    assert inventory.total_entries == len(inventory.entries)
    assert inventory.total_entries >= 1

    source_paths = tuple(entry.source_path for entry in inventory.entries)
    assert len(set(source_paths)) == len(source_paths)

    for entry in inventory.entries:
        assert entry.discovered is True
        assert entry.storage_node_id.startswith("storage_node_")
        assert entry.retrieval_source_id.startswith("retrieval_source_")
        assert entry.dashboard_exposure_id.startswith("panel_")
        assert entry.observability_binding_id.startswith("observability_")
