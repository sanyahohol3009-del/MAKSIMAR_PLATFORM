from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_existing_domain_inventory,
    build_existing_domain_minimal_manifest_contract,
)


def test_existing_domain_minimal_manifest_builder_smoke() -> None:
    inventory = build_existing_domain_inventory()
    contract = build_existing_domain_minimal_manifest_contract(inventory)

    assert contract.total_entries == inventory.total_entries
    assert contract.total_entries == len(contract.entries)

    for entry in contract.entries:
        assert entry.module_kind == "extension_cube"
        assert entry.storage_profile == "portable_storage"
        assert entry.retrieval_profile == "metadata_retrieval"
        assert entry.manifest_ready is True
