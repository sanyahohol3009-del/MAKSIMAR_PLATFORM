from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_contract,
)


def test_storage_registry_models_smoke() -> None:
    contract = build_storage_registry_contract()

    assert contract.total_entries == len(contract.entries)
    assert contract.dashboard_visible_entries >= 1
    assert contract.nas_ready_entries == contract.total_entries
