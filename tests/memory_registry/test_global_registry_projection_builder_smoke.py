from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_global_registry_projection_contract,
)


def test_global_registry_projection_builder_smoke() -> None:
    contract = build_global_registry_projection_contract()

    assert contract.total_entries == len(contract.entries)
    assert contract.dashboard_visible_entries == sum(
        1 for entry in contract.entries if entry.dashboard_visible
    )
    assert contract.retrieval_visible_entries == sum(
        1 for entry in contract.entries if entry.retrieval_visible
    )
    assert contract.observability_visible_entries == sum(
        1 for entry in contract.entries if entry.observability_visible
    )
