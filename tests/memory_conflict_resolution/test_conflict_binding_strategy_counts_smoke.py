from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_conflict_binding_contract,
)


def test_conflict_binding_strategy_counts_smoke() -> None:
    contract = build_conflict_binding_contract()

    assert contract.promote_new_version_bindings == 1
    assert contract.keep_existing_bindings == 1

    for entry in contract.entries:
        if entry.resolution_strategy == "promote_new_version":
            assert entry.version_incremented is True
        if entry.resolution_strategy == "keep_existing_record":
            assert entry.version_incremented is False
