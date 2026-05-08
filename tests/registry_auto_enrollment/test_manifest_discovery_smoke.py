from __future__ import annotations

from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_manifest_discovery_contract,
)


def test_manifest_discovery_smoke() -> None:
    contract = build_manifest_discovery_contract()

    assert contract.total_entries == len(contract.entries)
    assert contract.total_entries == (
        contract.existing_manifest_entries + contract.missing_manifest_entries
    )

    for entry in contract.entries:
        assert entry.module_slug
        assert entry.source_path
        assert entry.manifest_path.endswith("manifest.json")
        assert entry.discovery_ready is True
